"""Mhai Chat API views."""

from __future__ import annotations

from celery import chord
from django.contrib.auth import get_user_model
from rest_framework import permissions, viewsets

from mhai_chat.api.serializers import (
    MhaiChatEvalEmotionsSerializer,
    MhaiChatEvalMentBertSerializer,
    MhaiChatEvalPsychBertSerializer,
    MhaiChatSerializer,
)
from mhai_chat.models import (
    MhaiChat,
    MhaiChatEvalEmotions,
    MhaiChatEvalMentBert,
    MhaiChatEvalPsychBert,
)
from mhai_chat.tasks.task_answers import (
    finish_answering,
    process_chat_answer,
)
from mhai_chat.tasks.task_evaluations import (
    evaluate_emotions,
    evaluate_mentbert,
    evaluate_psychbert,
)

User = get_user_model()


class MhaiChatViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing chat messages in MhaiChat.
    """

    serializer_class = MhaiChatSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            queryset = MhaiChat.objects.filter(user=user).order_by(
                "prompt_timestamp"
            )
            since_id = self.request.query_params.get("since_id")
            if since_id:
                queryset = queryset.filter(id__gt=since_id)
            return queryset
        return MhaiChat.objects.none()

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


class MhaiChatEvalEmotionsViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing emotion analysis scores in MhaiChatEvalEmotions.
    """

    queryset = MhaiChatEvalEmotions.objects.all()
    serializer_class = MhaiChatEvalEmotionsSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return MhaiChatEvalEmotions.objects.filter(mhai_chat__user=user)
        return MhaiChatEvalEmotions.objects.none()


class MhaiChatEvalMentBertViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing MentBERT analysis scores linked to MhaiChat.
    """

    queryset = MhaiChatEvalMentBert.objects.all()
    serializer_class = MhaiChatEvalMentBertSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return MhaiChatEvalMentBert.objects.filter(mhai_chat__user=user)
        return MhaiChatEvalMentBert.objects.none()


class MhaiChatEvalPsychBertViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing PsychBERT analysis scores linked to MhaiChat.
    """

    queryset = MhaiChatEvalPsychBert.objects.all()
    serializer_class = MhaiChatEvalPsychBertSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return MhaiChatEvalPsychBert.objects.filter(mhai_chat__user=user)
        return MhaiChatEvalPsychBert.objects.none()
