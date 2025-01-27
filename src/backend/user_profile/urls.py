"""User Profile urls.py"""

from django.urls import path

from user_profile import views

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
]
