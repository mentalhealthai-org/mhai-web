"""User Profile urls.py"""

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from ai_profile import views
from ai_profile.api import views as views_api

# Define a router for API endpoints
router = DefaultRouter()
router.register(
    r"",
    views_api.AIProfileGeneralInfoView,
    basename="ai-profile-general",
)
router.register(
    r"interests",
    views_api.AIProfileInterestsView,
    basename="ai-profile-interests",
)
router.register(
    r"emotions",
    views_api.AIProfileEmotionsView,
    basename="ai-profile-emotions",
)
router.register(
    r"bio",
    views_api.AIProfileBiographyView,
    basename="ai-profile-bio",
)

urlpatterns = [
    path(
        "profile/",
        views.AIProfileView.as_view(),
        name="ai-profile-general",
    ),
    path(
        "profile/bio/",
        views.AIProfileView.as_view(),
        name="ai-profile-bio",
    ),
    path(
        "profile/emotions/",
        views.AIProfileView.as_view(),
        name="ai-profile-emotions",
    ),
    path(
        "profile/interests/",
        views.AIProfileView.as_view(),
        name="ai-profile-interests",
    ),
    path("profile/api/", include(router.urls)),
]
