"""User Profile urls.py"""

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from user_profile import views
from user_profile.api import views as views_api

# Define a router for API endpoints
router = DefaultRouter()
router.register(
    r"",
    views_api.UserProfileGeneralInfoView,
    basename="user-profile-general",
)
router.register(
    r"interests",
    views_api.UserProfileInterestsView,
    basename="user-profile-interests",
)
router.register(
    r"emotions",
    views_api.UserProfileEmotionsView,
    basename="user-profile-emotions",
)
router.register(
    r"bio",
    views_api.UserProfileBiographyView,
    basename="user-profile-bio",
)
router.register(
    r"critical-events",
    views_api.UserProfileCriticalEventView,
    basename="user-profile-events",
)


urlpatterns = [
    path(
        "profile/",
        views.UserProfileView.as_view(),
        name="user-profile-general",
    ),
    path(
        "profile/bio/",
        views.UserProfileView.as_view(),
        name="user-profile-bio",
    ),
    path(
        "profile/emotions/",
        views.UserProfileView.as_view(),
        name="user-profile-emotions",
    ),
    path(
        "profile/interests/",
        views.UserProfileView.as_view(),
        name="user-profile-interests",
    ),
    path(
        "profile/critical-events/",
        views.UserProfileView.as_view(),
        name="user-profile-events",
    ),
    path("profile/api/", include(router.urls)),
]
