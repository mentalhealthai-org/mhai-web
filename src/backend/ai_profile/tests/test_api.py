"""Test user profile API."""

import pytest

from django.contrib.auth import get_user_model
from django.urls import reverse
from mhai_web.users.models import User as UserClass
from rest_framework import status

from ai_profile.models import (
    AIProfile,
    GenderChoices,
)

User = get_user_model()


@pytest.fixture
def ai_profile(user: UserClass):
    """Fixture to create a test AIProfile instance linked to the user."""
    return AIProfile.objects.create(
        user=user,
        age=40,
        gender=GenderChoices.MALE,
        interests="video games, board games, nature",
        emotions="calm, workaholic",
        bio_life="Life description here.",
        bio_education="Education details here.",
        bio_work="Work experience here.",
        bio_family="Family background here.",
        bio_friends="Friends details here.",
        bio_pets="Pets details here.",
        bio_health="Health details here.",
    )


@pytest.mark.django_db
def test_update_ai_profile_general_info(api_client, user, ai_profile):
    """Test updating general information in the AIProfile model."""
    api_client.force_authenticate(user=user)
    url = reverse("ai-profile-general-detail", args=[ai_profile.id])
    data = {"age": 41, "gender": GenderChoices.FEMALE, "custom_gender": ""}
    response = api_client.patch(url, data, format="json")
    assert response.status_code == status.HTTP_200_OK
    ai_profile.refresh_from_db()
    assert ai_profile.age == 41  # noqa: PLR2004
    assert ai_profile.gender == GenderChoices.FEMALE


@pytest.mark.django_db
def test_update_ai_profile_interests(api_client, user, ai_profile):
    """Test updating interests in the AIProfile model."""
    api_client.force_authenticate(user=user)
    url = reverse("ai-profile-interests-detail", args=[ai_profile.id])
    data = {"interests": "video games, nature, hiking"}
    response = api_client.patch(url, data, format="json")
    assert response.status_code == status.HTTP_200_OK
    ai_profile.refresh_from_db()
    assert ai_profile.interests == "video games, nature, hiking"


@pytest.mark.django_db
def test_update_ai_profile_emotions(api_client, user, ai_profile):
    """Test updating emotional profile in the AIProfile model."""
    api_client.force_authenticate(user=user)
    url = reverse("ai-profile-emotions-detail", args=[ai_profile.id])
    data = {"emotions": "passionate, dedicated"}
    response = api_client.patch(url, data, format="json")
    assert response.status_code == status.HTTP_200_OK
    ai_profile.refresh_from_db()
    assert ai_profile.emotions == "passionate, dedicated"


@pytest.mark.django_db
def test_update_ai_profile_biography(api_client, user, ai_profile):
    """Test updating biography fields in the AIProfile model."""
    api_client.force_authenticate(user=user)
    url = reverse("ai-profile-bio-detail", args=[ai_profile.id])
    data = {
        "bio_life": "Updated life description.",
        "bio_education": "Updated education details.",
        "bio_work": "Updated work experience.",
        "bio_family": "Updated family background.",
        "bio_friends": "Updated friends details.",
        "bio_pets": "Updated pets details.",
        "bio_health": "Updated health details.",
    }
    response = api_client.patch(url, data, format="json")
    assert response.status_code == status.HTTP_200_OK
    ai_profile.refresh_from_db()
    assert ai_profile.bio_life == "Updated life description."
    assert ai_profile.bio_education == "Updated education details."
    assert ai_profile.bio_work == "Updated work experience."
