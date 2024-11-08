"""Test configuration module."""

from pathlib import Path

import pytest
import yaml

from ai_profile.models import AIProfile
from mhai_web.users.models import User
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from user_profile.models import UserProfile


@pytest.fixture
def user(db) -> User:
    """Return a user as fixture"""
    return User.objects.create_user(
        email="test@mymhai.com",
        password="password",  # noqa: S106
    )


@pytest.fixture
def ai_profile(db, user) -> AIProfile:
    """Return a AI profile as fixture."""
    profile_path = (
        Path(__file__).parent
        / "ai_profile"
        / "tests"
        / "data"
        / "ai_profile.yaml"
    )

    with Path.open(profile_path) as f:
        profile_data = yaml.safe_load(f)

    gender = (
        "M"
        if profile_data["gender"] == "male"
        else "F"
        if profile_data["gender"] == "female"
        else "O"
    )

    profiles = AIProfile.objects.filter(user=user)

    profiles.update(
        user=user,
        name=profile_data["name"],
        age=profile_data["age"],
        gender=gender,
        interests=profile_data["interests"],
        emotions=profile_data["emotions"],
        bio_life=profile_data["bio"]["life"],
        bio_education=profile_data["bio"]["education"],
        bio_work=profile_data["bio"]["work"],
        bio_family=profile_data["bio"]["family"],
        bio_friends=profile_data["bio"]["friends"],
        bio_pets=profile_data["bio"]["pets"],
        bio_health=profile_data["bio"]["health"],
    )

    profile = profiles.first()

    if not profile:
        raise Exception("No ai user profile available for given user.")

    return profile


@pytest.fixture
def user_profile(db, user) -> UserProfile:
    """Return a user profile as fixture."""
    profile_path = (
        Path(__file__).parent
        / "user_profile"
        / "tests"
        / "data"
        / "user_profile.yaml"
    )

    with Path.open(profile_path) as f:
        profile_data = yaml.safe_load(f)

    gender = (
        "M"
        if profile_data["gender"] == "male"
        else "F"
        if profile_data["gender"] == "female"
        else "O"
    )

    profiles = UserProfile.objects.filter(user=user)

    profiles.update(
        name=profile_data["name"],
        age=profile_data["age"],
        gender=gender,
        interests=profile_data["interests"],
        emotions=profile_data["emotions"],
        bio_life=profile_data["bio"]["life"],
        bio_education=profile_data["bio"]["education"],
        bio_work=profile_data["bio"]["work"],
        bio_family=profile_data["bio"]["family"],
        bio_friends=profile_data["bio"]["friends"],
        bio_pets=profile_data["bio"]["pets"],
        bio_health=profile_data["bio"]["health"],
    )
    profile = profiles.first()

    if not profile:
        raise Exception("No user profile available for given user.")

    return profile


@pytest.fixture
def api_client():
    """Fixture for creating an API client."""
    return APIClient()


@pytest.fixture
def auth_client(api_client, user):
    """Fixture for authenticating the API client."""
    token = Token.objects.create(user=user)
    api_client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")
    return api_client
