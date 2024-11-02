"""Test for user profile module."""

import pytest

from mhai_web.users.models import User

from ai_profile.models import (
    AIProfile,
    GenderChoices,
)


@pytest.mark.django_db
def test_ai_profile_creation(user: User):
    age = 40
    gender = GenderChoices.MALE
    interests = "video games, board games, nature"
    emotions = "calm, workaholic"
    bio_life = "Life description here."
    bio_education = "Education details here."
    bio_work = "Work experience here."
    bio_family = "Family background here."
    bio_friends = "Friends details here."
    bio_pets = "Pets details here."
    bio_health = "Health details here."

    profile = AIProfile.objects.create(
        user=user,
        age=age,
        gender=gender,
        interests=interests,
        emotions=emotions,
        bio_life=bio_life,
        bio_education=bio_education,
        bio_work=bio_work,
        bio_family=bio_family,
        bio_friends=bio_friends,
        bio_pets=bio_pets,
        bio_health=bio_health,
    )
    assert profile.age == age
    assert profile.gender == gender
    assert profile.interests == interests
    assert profile.emotions == emotions
    assert profile.bio_life == bio_life
    assert profile.bio_education == bio_education
    assert profile.bio_work == bio_work
    assert profile.bio_family == bio_family
    assert profile.bio_friends == bio_friends
    assert profile.bio_pets == bio_pets
    assert profile.bio_health == bio_health


@pytest.mark.django_db
def test_ai_profile_custom_gender(user: User):
    profile = AIProfile.objects.create(
        user=user,
        age=28,
        gender=GenderChoices.CUSTOM,
        gender_custom="Genderqueer",
    )
    assert profile.gender == GenderChoices.CUSTOM
    assert profile.gender_custom == "Genderqueer"

    # Changing gender to non-custom should clear gender_custom
    profile.gender = GenderChoices.FEMALE
    profile.gender_custom = ""
    profile.save()
    assert profile.gender_custom == ""
