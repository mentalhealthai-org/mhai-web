"""Serializers for mhai_chat."""

from __future__ import annotations

from rest_framework import serializers

from mhai_chat.models import (
    MhaiChat,
    MhaiChatEvalEmotions,
    MhaiChatEvalMentBert,
    MhaiChatEvalPsychBert,
)


class MhaiChatSerializer(serializers.ModelSerializer):
    """Serializer for the MhaiChat model."""

    class Meta:
        model = MhaiChat
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


class MhaiChatEvalMentBertSerializer(serializers.ModelSerializer):
    """Serializer for the MhaiChatEvalMentBert model."""

    class Meta:
        model = MhaiChatEvalMentBert
        fields = [
            "id",
            "mhai_chat",
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


class MhaiChatEvalPsychBertSerializer(serializers.ModelSerializer):
    """Serializer for the MhaiChatEvalPsychBert model."""

    class Meta:
        model = MhaiChatEvalPsychBert
        fields = [
            "id",
            "mhai_chat",
            "unrelated",
            "mental_illnesses",
            "anxiety",
            "depression",
            "social_anxiety",
            "loneliness",
        ]


class MhaiChatEvalEmotionsSerializer(serializers.ModelSerializer):
    """
    Serializer for the MhaiChatEvalEmotions model.

    It stores emotion analysis scores.
    """

    class Meta:
        model = MhaiChatEvalEmotions
        fields = [
            "id",
            "mhai_chat",
            "neutral",
            "joy",
            "disgust",
            "sadness",
            "anger",
            "surprise",
            "fear",
        ]
