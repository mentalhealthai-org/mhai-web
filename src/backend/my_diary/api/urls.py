"""Mhai Chat API urls."""

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from my_diary.api.views import (
    MhaiDiaryEvalEmotionsViewSet,
    MhaiDiaryEvalMentBertViewSet,
    MhaiDiaryEvalPsychBertViewSet,
    MhaiDiaryViewSet,
)

router = DefaultRouter()
router.register(r"", MhaiDiaryViewSet, basename="mhai-diary")
router.register(
    r"eval/mentbert",
    MhaiDiaryEvalMentBertViewSet,
    basename="mhai-diary-eval-mentbert",
)
router.register(
    r"eval/psychbert",
    MhaiDiaryEvalPsychBertViewSet,
    basename="mhai-diary-eval-psychbert",
)
router.register(
    r"eval/emotions",
    MhaiDiaryEvalEmotionsViewSet,
    basename="mhai-diary-eval-emotions",
)

urlpatterns = [
    path("", include(router.urls)),
]
