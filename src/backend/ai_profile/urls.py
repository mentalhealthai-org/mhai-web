"""User Profile urls.py"""

from django.urls import path

from ai_profile import views

urlpatterns = [
    path(
        "ai-profile/",
        views.AIProfileView.as_view(),
        name="ai-profile-general",
    ),
    path(
        "ai-profile/bio/",
        views.AIProfileView.as_view(),
        name="ai-profile-bio",
    ),
    path(
        "ai-profile/emotions/",
        views.AIProfileView.as_view(),
        name="ai-profile-emotions",
    ),
    path(
        "ai-profile/interests/",
        views.AIProfileView.as_view(),
        name="ai-profile-interests",
    ),
]
