"""User Profile urls.py"""

from django.urls import include, path
from django.views.generic import TemplateView
from rest_framework.routers import DefaultRouter

from user_profile.api import views

# Define a router for API endpoints
router = DefaultRouter()
router.register(
    r"",
    views.UserProfileGeneralInfoView,
    basename="user-profile-general",
)
router.register(
    r"interests",
    views.UserProfileInterestsView,
    basename="user-profile-interests",
)
router.register(
    r"emotions",
    views.UserProfileEmotionalProfileView,
    basename="user-profile-emotions",
)
router.register(
    r"bio",
    views.UserProfileBiographyView,
    basename="user-profile-bio",
)
router.register(
    r"events",
    views.UserProfileCriticalEventView,
    basename="user-profile-events",
)


urlpatterns = [
    path(
        "profile/",
        TemplateView.as_view(template_name="generic.html"),
        name="user-profile-general",
    ),
    path(
        "profile/bio/",
        TemplateView.as_view(template_name="generic.html"),
        name="user-profile-bio",
    ),
    path(
        "profile/emotions/",
        TemplateView.as_view(template_name="generic.html"),
        name="user-profile-emotions",
    ),
    path(
        "profile/interests/",
        TemplateView.as_view(template_name="generic.html"),
        name="user-profile-interests",
    ),
    path(
        "profile/events/",
        TemplateView.as_view(template_name="generic.html"),
        name="user-profile-events",
    ),
    path("profile/api/", include(router.urls)),
]
