"""User Profile Serializers."""

from rest_framework import serializers

from user_profile.models import UserProfile, UserProfileCriticalEvent


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = [
            "name",
            "age",
            "gender",
            "gender_custom",
            "interests",
            "emotions",
            "bio_life",
            "bio_education",
            "bio_work",
            "bio_family",
            "bio_friends",
            "bio_pets",
            "bio_health",
        ]


class UserProfileGeneralInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ["name", "age", "gender", "gender_custom"]


class UserProfileInterestsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ["interests"]


class UserProfileEmotionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ["emotions"]


class UserProfileBiographySerializer(serializers.ModelSerializer):
    bio_life = serializers.CharField(required=False, allow_blank=True)
    bio_education = serializers.CharField(required=False, allow_blank=True)
    bio_work = serializers.CharField(required=False, allow_blank=True)
    bio_family = serializers.CharField(required=False, allow_blank=True)
    bio_friends = serializers.CharField(required=False, allow_blank=True)
    bio_pets = serializers.CharField(required=False, allow_blank=True)
    bio_health = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = UserProfile
        fields = [
            "bio_life",
            "bio_education",
            "bio_work",
            "bio_family",
            "bio_friends",
            "bio_pets",
            "bio_health",
        ]


class UserProfileCriticalEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfileCriticalEvent
        fields = [
            "id",
            "profile",
            "date",
            "description",
            "impact",
            "resolved",
            "treated",
        ]
