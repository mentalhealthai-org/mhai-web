"""Test user profile API."""

from datetime import date

import pytest

from django.contrib.auth import get_user_model
from django.urls import reverse
from mhai_web.users.models import User as UserClass
from rest_framework import status

from user_profile.models import (
    GenderChoices,
    UserProfile,
    UserProfileCriticalEvent,
)

User = get_user_model()


@pytest.fixture
def user_profile(user: UserClass):
    """Fixture to create a test UserProfile instance linked to the user."""
    profiles = UserProfile.objects.filter(user=user)

    profiles.update(
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

    return UserProfile.objects.get(user=user)


@pytest.mark.django_db
def test_update_user_profile_general_info(api_client, user, user_profile):
    """Test updating general information in the UserProfile model."""
    api_client.force_authenticate(user=user)
    url = reverse("user-profile-general-detail", args=[user_profile.id])
    data = {"age": 41, "gender": GenderChoices.FEMALE, "custom_gender": ""}
    response = api_client.patch(url, data, format="json")
    assert response.status_code == status.HTTP_200_OK
    user_profile.refresh_from_db()
    assert user_profile.age == 41  # noqa: PLR2004
    assert user_profile.gender == GenderChoices.FEMALE


@pytest.mark.django_db
def test_update_user_profile_interests(api_client, user, user_profile):
    """Test updating interests in the UserProfile model."""
    api_client.force_authenticate(user=user)
    url = reverse("user-profile-interests-detail", args=[user_profile.id])
    data = {"interests": "video games, nature, hiking"}
    response = api_client.patch(url, data, format="json")
    assert response.status_code == status.HTTP_200_OK
    user_profile.refresh_from_db()
    assert user_profile.interests == "video games, nature, hiking"


@pytest.mark.django_db
def test_update_user_profile_emotions(api_client, user, user_profile):
    """Test updating emotional profile in the UserProfile model."""
    api_client.force_authenticate(user=user)
    url = reverse("user-profile-emotions-detail", args=[user_profile.id])
    data = {"emotions": "passionate, dedicated"}
    response = api_client.patch(url, data, format="json")
    assert response.status_code == status.HTTP_200_OK
    user_profile.refresh_from_db()
    assert user_profile.emotions == "passionate, dedicated"


@pytest.mark.django_db
def test_update_user_profile_biography(api_client, user, user_profile):
    """Test updating biography fields in the UserProfile model."""
    api_client.force_authenticate(user=user)
    url = reverse("user-profile-bio-detail", args=[user_profile.id])
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
    user_profile.refresh_from_db()
    assert user_profile.bio_life == "Updated life description."
    assert user_profile.bio_education == "Updated education details."
    assert user_profile.bio_work == "Updated work experience."


@pytest.mark.django_db
def test_create_user_profile_important_event(api_client, user, user_profile):
    """Test creating a UserProfileCriticalEvent for the UserProfile model."""
    api_client.force_authenticate(user=user)
    url = reverse("user-profile-events-list")
    data = {
        "profile": user_profile.id,
        "date": date(2022, 1, 1),
        "description": "Significant life event.",
        "impact": "Major impact on user.",
        "resolved": False,
        "treated": False,
    }
    response = api_client.post(url, data, format="json")
    # TODO: not fully implemented
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


@pytest.mark.django_db
def test_update_user_profile_important_event(api_client, user, user_profile):
    """Test updating an existing UserProfileCriticalEvent."""
    api_client.force_authenticate(user=user)
    event = UserProfileCriticalEvent.objects.create(
        profile=user_profile,
        date=date(2022, 1, 1),
        description="Significant life event.",
        impact="Major impact on user.",
        resolved=False,
        treated=False,
    )
    url = reverse("user-profile-events-detail", args=[event.id])
    data = {"resolved": True}
    response = api_client.patch(url, data, format="json")
    assert response.status_code == status.HTTP_200_OK
    event.refresh_from_db()
    assert event.resolved is True


@pytest.mark.django_db
def test_delete_user_profile_important_event(api_client, user, user_profile):
    """Test deleting a UserProfileCriticalEvent."""
    api_client.force_authenticate(user=user)
    event = UserProfileCriticalEvent.objects.create(
        profile=user_profile,
        date=date(2022, 1, 1),
        description="Significant life event.",
        impact="Major impact on user.",
        resolved=False,
        treated=False,
    )
    url = reverse("user-profile-events-detail", args=[event.id])
    response = api_client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert UserProfileCriticalEvent.objects.filter(id=event.id).count() == 0
