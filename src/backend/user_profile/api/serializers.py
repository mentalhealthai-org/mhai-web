"""User Profile Serializers."""

from rest_framework import serializers

from user_profile.models import UserProfile, UserProfileCriticalEvent


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
