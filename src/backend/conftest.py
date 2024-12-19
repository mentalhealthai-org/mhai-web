"""Test configuration module."""

from datetime import timedelta
from pathlib import Path

import pytest
import yaml

from ai_profile.models import AIProfile
from django.utils.timezone import now
from mhai_chat.models import (
    MhaiChat,
    MhaiChatEvalEmotions,
    MhaiChatEvalMentBert,
    MhaiChatEvalPsychBert,
)
from mhai_web.users.models import User
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from user_profile.models import UserProfile


@pytest.fixture
@pytest.mark.django_db
def user(db) -> User:
    """Return a user as fixture"""
    return User.objects.create_user(
        email="test@mymhai.com",
        password="password",  # noqa: S106
    )


@pytest.fixture
@pytest.mark.django_db
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
@pytest.mark.django_db
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


@pytest.fixture
@pytest.mark.django_db
def chat_data(db, user: User):
    """Fixture to create initial test data for the models."""
    user_id = user.id
    chat1 = MhaiChat.objects.create(
        user_id=user_id,
        prompt="How are you?",
        response="I'm fine.",
        status="completed",
        prompt_timestamp=now() - timedelta(days=3),
    )
    chat2 = MhaiChat.objects.create(
        user_id=user_id,
        prompt="Tell me a joke.",
        response="Why did the chicken cross the road?",
        status="completed",
        prompt_timestamp=now() - timedelta(days=2),
    )
    chat3 = MhaiChat.objects.create(
        user_id=user_id,
        prompt="What is AI?",
        response="AI stands for artificial intelligence.",
        status="completed",
        prompt_timestamp=now() - timedelta(days=1),
    )

    MhaiChatEvalEmotions.objects.create(
        mhai_chat=chat1,
        fear=0.1,
        sadness=0.2,
        neutral=0.5,
        joy=0.2,
        surprise=0.0,
        anger=0.0,
        disgust=0.0,
    )
    MhaiChatEvalEmotions.objects.create(
        mhai_chat=chat2,
        fear=0.0,
        sadness=0.0,
        neutral=0.3,
        joy=0.6,
        surprise=0.1,
        anger=0.0,
        disgust=0.0,
    )
    MhaiChatEvalEmotions.objects.create(
        mhai_chat=chat3,
        fear=0.2,
        sadness=0.1,
        neutral=0.3,
        joy=0.3,
        surprise=0.0,
        anger=0.1,
        disgust=0.0,
    )

    MhaiChatEvalMentBert.objects.create(
        mhai_chat=chat1,
        borderline=0.1,
        anxiety=0.2,
        depression=0.3,
        bipolar=0.0,
        ocd=0.4,
        adhd=0.1,
        schizophrenia=0.2,
        asperger=0.0,
        ptsd=0.2,
    )
    MhaiChatEvalMentBert.objects.create(
        mhai_chat=chat2,
        borderline=0.0,
        anxiety=0.1,
        depression=0.2,
        bipolar=0.1,
        ocd=0.3,
        adhd=0.4,
        schizophrenia=0.1,
        asperger=0.2,
        ptsd=0.1,
    )
    MhaiChatEvalMentBert.objects.create(
        mhai_chat=chat3,
        borderline=0.2,
        anxiety=0.0,
        depression=0.1,
        bipolar=0.3,
        ocd=0.2,
        adhd=0.0,
        schizophrenia=0.4,
        asperger=0.1,
        ptsd=0.3,
    )

    MhaiChatEvalPsychBert.objects.create(
        mhai_chat=chat1,
        unrelated=0.3,
        mental_illnesses=0.2,
        anxiety=0.1,
        depression=0.2,
        social_anxiety=0.2,
        loneliness=0.1,
    )
    MhaiChatEvalPsychBert.objects.create(
        mhai_chat=chat2,
        unrelated=0.2,
        mental_illnesses=0.1,
        anxiety=0.0,
        depression=0.3,
        social_anxiety=0.4,
        loneliness=0.2,
    )
    MhaiChatEvalPsychBert.objects.create(
        mhai_chat=chat3,
        unrelated=0.1,
        mental_illnesses=0.3,
        anxiety=0.2,
        depression=0.1,
        social_anxiety=0.0,
        loneliness=0.4,
    )
