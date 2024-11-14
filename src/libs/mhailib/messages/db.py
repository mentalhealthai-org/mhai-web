"""DB module provides functions that access the database."""

from __future__ import annotations

from datetime import datetime, timedelta
from typing import Any

from ai_profile.api.serializers import AIProfileSerializer
from ai_profile.models import AIProfile
from mhai_chat.api.serializers import (
    MhaiChatEvalEmotionsSerializer,
    MhaiChatEvalMentBertSerializer,
    MhaiChatEvalPsychBertSerializer,
    MhaiChatSerializer,
)
from mhai_chat.models import MhaiChat, MhaiChatEvalEmotions
from user_profile.api.serializers import UserProfileSerializer
from user_profile.models import UserProfile


def get_ai_profile(user_id: int) -> dict[str, Any]:
    ai_profile = AIProfile.objects.get(user_id=user_id)
    return AIProfileSerializer(ai_profile).data


def get_user_profile(user_id: int) -> dict[str, Any]:
    user_profile = UserProfile.objects.get(id=user_id)
    return UserProfileSerializer(user_profile).data


def load_conversation_history(user_id: int) -> list[dict[str, Any]]:
    """
    Load the conversation history for a given user using the MhaiChat model.

    Parameters
    ----------
    user_id : int
        The ID of the user whose conversation history is to be retrieved.

    Returns
    -------
    list[dict[str, Any]]
        A list of dictionaries containing user and assistant messages
        with roles "user" or "assistant".
    """
    messages = MhaiChat.objects.filter(user_id=user_id).order_by("timestamp")

    history = []
    for message in messages:
        history.append({"role": "user", "content": message.user_input})
        history.append({"role": "assistant", "content": message.ai_response})

    return history


def load_emotions(user_id: int) -> list[dict[str, Any]]:
    """
    Load the emotion analysis scores.

    This function loads emotion's score for a given user's chat messages
    using the MhaiChatEvalEmotions model.

    Parameters
    ----------
    user_id : int
        The ID of the user whose emotion analysis scores are to be retrieved.

    Returns
    -------
    list[dict[str, Any]]
        A list of dictionaries, each containing emotion scores for a specific
        chat message.
    """
    emotion_scores = MhaiChatEvalEmotions.objects.filter(
        mhai_chat__user_id=user_id
    )

    return [
        MhaiChatEvalEmotionsSerializer(emotion).data
        for emotion in emotion_scores
    ]


def get_emotions_top_3(data: list[dict[str, Any]]) -> list[dict[str, Any]]:
    for row in data:
        emotions = {
            "neutral": row["neutral"],
            "joy": row["joy"],
            "disgust": row["disgust"],
            "sadness": row["sadness"],
            "anger": row["anger"],
            "surprise": row["surprise"],
            "fear": row["fear"],
        }
        top_emotions = sorted(
            emotions.items(), key=lambda x: x[1], reverse=True
        )

        if top_emotions[0][1] > 0.75:
            for emotion in emotions:
                row[emotion] = 1 if emotion == top_emotions[0][0] else 0
        else:
            top_3_emotions = [emotion[0] for emotion in top_emotions[:3]]
            for emotion in emotions:
                row[emotion] = 1 if emotion in top_3_emotions else 0

    return data


def load_conversation_history_last_24h(user_id: int) -> list[dict[str, Any]]:
    """
    Load the conversation history and evaluations from the last 24 hours.

    Parameters
    ----------
    user_id : int
        The ID of the user whose conversation history is to be retrieved.

    Returns
    -------
    list[dict[str, Any]]
        A list of dictionaries containing user messages, AI responses,
        and associated evaluation scores.
    """
    last_24h = datetime.now() - timedelta(days=1)

    chat_entries = MhaiChat.objects.filter(
        user_id=user_id, timestamp__gte=last_24h
    )

    history_data = []

    for chat in chat_entries:
        chat_data = MhaiChatSerializer(chat).data

        emotions_data = (
            MhaiChatEvalEmotionsSerializer(chat.mhaichatevalemotions).data
            if hasattr(chat, "mhaichatevalemotions")
            else {}
        )
        mentbert_data = (
            MhaiChatEvalMentBertSerializer(chat.mhaichatevalmentbert).data
            if hasattr(chat, "mhaichatevalmentbert")
            else {}
        )
        psychbert_data = (
            MhaiChatEvalPsychBertSerializer(chat.mhaichatevalpsychbert).data
            if hasattr(chat, "mhaichatevalpsychbert")
            else {}
        )

        chat_data.update(
            {
                "emotions": emotions_data,
                "mentbert": mentbert_data,
                "psychbert": psychbert_data,
            }
        )

        history_data.append(chat_data)

    return history_data
