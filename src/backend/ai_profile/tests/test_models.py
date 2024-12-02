"""Test for user profile module."""

import secrets

import pytest

from mhai_web.users.models import User

from ai_profile.models import (
    AIProfile,
    GenderChoices,
)


@pytest.mark.django_db
def test_ai_profile_creation():
    """
    Test the AI profile creation.

    When a user is created, automatically the ai profile is created.
    """
    password = secrets.token_urlsafe(12)
    user = User.objects.create(email="yoda@mymhai.com", password=password)

    name = "Yoda"
    age = 900
    gender = GenderChoices.MALE
    interests = """
        Teaching young Jedi, meditation, studying the Force,
        lightsaber combat, philosophy, and peacekeeping.
    """
    emotions = """
    Wise, calm, patient, compassionate, occasionally somber
    due to the state of the galaxy.
    """
    bio_life = """
    A legendary Jedi Master with over 800 years of experience,
    known for his wisdom and powerful connection to the Force.
    Yoda has played a pivotal role in the history of the galaxy,
    guiding the Jedi Order through times of peace and conflict.
    """
    bio_education = """
    Studied the mysteries of the Force extensively, mastering Jedi
    teachings and philosophies. Spent centuries learning and teaching
    at the Jedi Temple on Coruscant.
    """
    bio_work = """
    Served as the Grand Master of the Jedi Order, leading the Jedi Council.
    Trained generations of Jedi Knights, including notable figures like
    Luke Skywalker and Count Dooku.
    """
    bio_family = """
    Little is known about Yoda's species or family background, shrouded in
    mystery and rarely discussed even among close allies.
    """
    bio_friends = """
    Maintained close relationships with fellow Jedi such as Mace Windu,
    Obi-Wan Kenobi, and other members of the Jedi Council. Valued
    friendship and mentorship highly.
    """
    bio_pets = """
    Has no known pets but possesses a deep connection with all living
    beings through the Force.
    """
    bio_health = """
    Despite his advanced age and small stature, Yoda remains remarkably
    agile and strong. His health is sustained by his profound mastery of
    the Force, allowing him to perform feats that belie his physical
    appearance.
    """

    profiles = AIProfile.objects.filter(user=user)
    profiles.update(
        name=name,
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

    profile = AIProfile.objects.get(user=user)

    assert profile.name == name
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
    profile = AIProfile.objects.get(user=user)

    profile.age = 28
    profile.gender = GenderChoices.CUSTOM
    profile.gender_custom = "Genderqueer"
    profile.save()

    profile, _ = AIProfile.objects.get_or_create(user=user)

    assert profile.gender == GenderChoices.CUSTOM
    assert profile.gender_custom == "Genderqueer"

    # Changing gender to non-custom should clear gender_custom
    profile.gender = GenderChoices.FEMALE
    profile.gender_custom = ""
    profile.save()

    profile = AIProfile.objects.get(user=user)

    assert profile.gender_custom == ""
