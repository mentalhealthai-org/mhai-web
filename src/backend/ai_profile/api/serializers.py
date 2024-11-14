"""User Profile Serializers."""

from rest_framework import serializers

from ai_profile.models import AIProfile


class AIProfileSerializer(serializers.ModelSerializer):
    """Complete serializer for the AIProfile."""

    class Meta:
        model = AIProfile
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


class AIProfileGeneralInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = AIProfile
        fields = ["name", "age", "gender", "gender_custom"]


class AIProfileInterestsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AIProfile
        fields = ["interests"]


class AIProfileEmotionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AIProfile
        fields = ["emotions"]


class AIProfileBiographySerializer(serializers.ModelSerializer):
    class Meta:
        model = AIProfile
        fields = [
            "bio_life",
            "bio_education",
            "bio_work",
            "bio_family",
            "bio_friends",
            "bio_pets",
            "bio_health",
        ]
