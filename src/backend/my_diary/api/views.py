"""Mhai Chat API views."""

from __future__ import annotations

from celery import chord
from django.contrib.auth import get_user_model
from rest_framework import permissions, viewsets

from my_diary.api.serializers import (
    MhaiDiaryEvalEmotionsSerializer,
    MhaiDiaryEvalMentBertSerializer,
    MhaiDiaryEvalPsychBertSerializer,
    MhaiDiarySerializer,
)
from my_diary.models import (
    MhaiDiaryEvalEmotions,
    MhaiDiaryEvalMentBert,
    MhaiDiaryEvalPsychBert,
    MyDiary,
)
from my_diary.tasks.task_answers import (
    finish_answering,
    process_chat_answer,
)
from my_diary.tasks.task_evaluations import (
    evaluate_emotions,
    evaluate_mentbert,
    evaluate_psychbert,
)

User = get_user_model()


class MhaiDiaryViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing chat messages in MyDiary.
    """

    serializer_class = MhaiDiarySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            queryset = MyDiary.objects.filter(user=user).order_by(
                "prompt_timestamp"
            )
            since_id = self.request.query_params.get("since_id")
            if since_id:
                queryset = queryset.filter(id__gt=since_id)
            return queryset
        return MyDiary.objects.none()

    def perform_create(self, serializer) -> None:
        user_id = self.request.user.id

        user = User.objects.get(id=user_id)

        serializer.save(user=user, status="started")

        message_id = serializer.instance.id

        task_question = process_chat_answer.s(
            message_id=message_id,
            user_id=user_id,
        )
        task_eval_emotions = evaluate_emotions.s(message_id)
        task_eval_mentbert = evaluate_mentbert.s(message_id)
        task_eval_psychbert = evaluate_psychbert.s(message_id)

        tasks = [
            task_question,
            task_eval_emotions,
            task_eval_mentbert,
            task_eval_psychbert,
        ]

        pipeline = chord(tasks, finish_answering.s(message_id))
        pipeline.apply_async()


class MhaiDiaryEvalEmotionsViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing emotion analysis scores in MhaiDiaryEvalEmotions.
    """

    queryset = MhaiDiaryEvalEmotions.objects.all()
    serializer_class = MhaiDiaryEvalEmotionsSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return MhaiDiaryEvalEmotions.objects.filter(my_diary__user=user)
        return MhaiDiaryEvalEmotions.objects.none()


class MhaiDiaryEvalMentBertViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing MentBERT analysis scores linked to MyDiary.
    """

    queryset = MhaiDiaryEvalMentBert.objects.all()
    serializer_class = MhaiDiaryEvalMentBertSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return MhaiDiaryEvalMentBert.objects.filter(my_diary__user=user)
        return MhaiDiaryEvalMentBert.objects.none()


class MhaiDiaryEvalPsychBertViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing PsychBERT analysis scores linked to MyDiary.
    """

    queryset = MhaiDiaryEvalPsychBert.objects.all()
    serializer_class = MhaiDiaryEvalPsychBertSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return MhaiDiaryEvalPsychBert.objects.filter(my_diary__user=user)
        return MhaiDiaryEvalPsychBert.objects.none()
