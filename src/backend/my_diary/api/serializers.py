"""Serializers for my_diary."""

from __future__ import annotations

from rest_framework import serializers

from my_diary.models import (
    MhaiDiary,
    MhaiDiaryEvalEmotions,
    MhaiDiaryEvalMentBert,
    MhaiDiaryEvalPsychBert,
)


class MhaiDiarySerializer(serializers.ModelSerializer):
    """Serializer for the MhaiDiary model."""

    class Meta:
        model = MhaiDiary
        fields = [
            "id",
            "user",
            "prompt",
            "response",
            "prompt_timestamp",
            "response_timestamp",
        ]
        read_only_fields = [
            "id",
            "response",
            "prompt_timestamp",
            "response_timestamp",
            "user",
        ]


class MhaiDiaryEvalMentBertSerializer(serializers.ModelSerializer):
    """Serializer for the MhaiDiaryEvalMentBert model."""

    class Meta:
        model = MhaiDiaryEvalMentBert
        fields = [
            "id",
            "my_diary",
            "borderline",
            "anxiety",
            "depression",
            "bipolar",
            "ocd",
            "adhd",
            "schizophrenia",
            "asperger",
            "ptsd",
        ]


class MhaiDiaryEvalPsychBertSerializer(serializers.ModelSerializer):
    """Serializer for the MhaiDiaryEvalPsychBert model."""

    class Meta:
        model = MhaiDiaryEvalPsychBert
        fields = [
            "id",
            "my_diary",
            "unrelated",
            "mental_illnesses",
            "anxiety",
            "depression",
            "social_anxiety",
            "loneliness",
        ]


class MhaiDiaryEvalEmotionsSerializer(serializers.ModelSerializer):
    """
    Serializer for the MhaiDiaryEvalEmotions model.

    It stores emotion analysis scores.
    """

    class Meta:
        model = MhaiDiaryEvalEmotions
        fields = [
            "id",
            "my_diary",
            "neutral",
            "joy",
            "disgust",
            "sadness",
            "anger",
            "surprise",
            "fear",
        ]
