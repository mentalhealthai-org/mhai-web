"""DB module provides functions that access the database."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any, cast

from ai_profile.api.serializers import AIProfileSerializer
from ai_profile.models import AIProfile
from my_diary.api.serializers import (
    MhaiDiaryEvalEmotionsSerializer,
    MhaiDiaryEvalMentBertSerializer,
    MhaiDiaryEvalPsychBertSerializer,
    MhaiDiarySerializer,
)
from my_diary.models import MyDiary
from user_profile.api.serializers import UserProfileSerializer
from user_profile.models import UserProfile


def get_ai_profile(user_id: int) -> dict[str, Any]:
    ai_profile = AIProfile.objects.get(user_id=user_id)
    return AIProfileSerializer(ai_profile).data


def get_user_profile(user_id: int) -> dict[str, Any]:
    user_profile = UserProfile.objects.get(user_id=user_id)
    return UserProfileSerializer(user_profile).data


def load_chat_history(user_id: int, last_k: int = 10) -> list[dict[str, Any]]:
    """
    Load the conversation history for a given user using the MyDiary model.

    Parameters
    ----------
    user_id : int
        The ID of the user whose conversation history is to be retrieved.
    last_k: int, default 10

    Returns
    -------
    list[dict[str, Any]]
        A list of dictionaries containing user and assistant messages
        with roles "user" or "assistant".
    """
    # TODO: this should be changed to RAG approach with top 10
    messages = MyDiary.objects.filter(
        user_id=user_id,
    ).order_by("prompt_timestamp")
    idx_start = max(0, len(messages) - last_k)
    messages = messages[idx_start:]

    history = []
    for message in messages:
        history.append({"role": "user", "content": message.prompt})
        history.append({"role": "assistant", "content": message.response})

    return history


def load_chat_and_evaluation_history_last_k(
    user_id: int, last_k: int = 10
) -> list[Mapping[str, Any]]:
    """
    Load the last k conversation history and its evaluations.

    Parameters
    ----------
    user_id : int
        The ID of the user whose conversation history is to be retrieved.

    Returns
    -------
    list[Mapping[str, Any]]
        A list of dictionaries containing user messages, AI responses,
        and associated evaluation scores.
    """
    chat_entries = MyDiary.objects.filter(user_id=user_id)[-last_k:]

    history_data = []

    for chat in chat_entries:
        chat_data = MhaiDiarySerializer(chat).data

        emotions_data = (
            MhaiDiaryEvalEmotionsSerializer(chat.mhaidiaryevalemotions).data
            if hasattr(chat, "mhaidiaryevalemotions")
            else {}
        )
        mentbert_data = (
            MhaiDiaryEvalMentBertSerializer(chat.mhaidiaryevalmentbert).data
            if hasattr(chat, "mhaidiaryevalmentbert")
            else {}
        )
        psychbert_data = (
            MhaiDiaryEvalPsychBertSerializer(chat.mhaidiaryevalpsychbert).data
            if hasattr(chat, "mhaidiaryevalpsychbert")
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

    return cast(list[Mapping[str, Any]], history_data)
