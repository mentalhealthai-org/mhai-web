"""Mhai Chat API views."""

from __future__ import annotations

from rest_framework import viewsets

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


class MhaiChatViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing chat messages in MhaiChat.
    """

    queryset = MhaiChat.objects.all()
    serializer_class = MhaiChatSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return MhaiChat.objects.filter(user=user)
        return MhaiChat.objects.none()


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
