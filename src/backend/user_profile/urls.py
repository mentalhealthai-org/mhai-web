"""User Profile urls.py"""

from django.urls import include, path
from django.views.generic import TemplateView
from rest_framework.routers import DefaultRouter

from user_profile.api import views

# Define a router for API endpoints
router = DefaultRouter()
router.register(
    r"profile/general",
    views.UserProfileGeneralInfoView,
    basename="user-profile-general",
)
router.register(
    r"profile/interests",
    views.UserProfileInterestsView,
    basename="user-profile-interests",
)
router.register(
    r"profile/emotions",
    views.UserProfileEmotionalProfileView,
    basename="user-profile-emotions",
)
router.register(
    r"profile/biography",
    views.UserProfileBiographyView,
    basename="user-profile-bio",
)
router.register(
    r"profile/events",
    views.UserProfileCriticalEventView,
    basename="user-profile-events",
)


urlpatterns = [
    path(
        "",
        TemplateView.as_view(template_name="generic.html"),
        name="user-profile-general",
    ),
    path(
        "bio/",
        TemplateView.as_view(template_name="generic.html"),
        name="user-profile-bio",
    ),
    path(
        "emotions/",
        TemplateView.as_view(template_name="generic.html"),
        name="user-profile-emotions",
    ),
    path(
        "interests/",
        TemplateView.as_view(template_name="generic.html"),
        name="user-profile-interests",
    ),
    path(
        "events/",
        TemplateView.as_view(template_name="generic.html"),
        name="user-profile-events",
    ),
    path("api/", include(router.urls)),
]
