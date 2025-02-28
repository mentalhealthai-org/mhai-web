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
router.register(r"", MhaiDiaryViewSet, basename="my-diary")
router.register(
    r"eval/mentbert",
    MhaiDiaryEvalMentBertViewSet,
    basename="my-diary-eval-mentbert",
)
router.register(
    r"eval/psychbert",
    MhaiDiaryEvalPsychBertViewSet,
    basename="my-diary-eval-psychbert",
)
router.register(
    r"eval/emotions",
    MhaiDiaryEvalEmotionsViewSet,
    basename="my-diary-eval-emotions",
)

urlpatterns = [
    path("", include(router.urls)),
]
