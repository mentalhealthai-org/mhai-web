"""Mhai Chat API urls."""

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from mhai_chat.api.views import (
    MhaiChatEvalEmotionsViewSet,
    MhaiChatEvalMentBertViewSet,
    MhaiChatEvalPsychBertViewSet,
    MhaiChatViewSet,
)

router = DefaultRouter()
router.register(r"", MhaiChatViewSet, basename="mhai-chat")
router.register(
    r"eval/mentbert",
    MhaiChatEvalMentBertViewSet,
    basename="mhai-chat-eval-mentbert",
)
router.register(
    r"eval/psychbert",
    MhaiChatEvalPsychBertViewSet,
    basename="mhai-chat-eval-psychbert",
)
router.register(
    r"eval/emotions",
    MhaiChatEvalEmotionsViewSet,
    basename="mhai-chat-eval-emotions",
)

urlpatterns = [
    path("", include(router.urls)),
]
