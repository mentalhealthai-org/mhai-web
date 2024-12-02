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
    bio_life = serializers.CharField(required=False, allow_blank=True)
    bio_education = serializers.CharField(required=False, allow_blank=True)
    bio_work = serializers.CharField(required=False, allow_blank=True)
    bio_family = serializers.CharField(required=False, allow_blank=True)
    bio_friends = serializers.CharField(required=False, allow_blank=True)
    bio_pets = serializers.CharField(required=False, allow_blank=True)
    bio_health = serializers.CharField(required=False, allow_blank=True)

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
