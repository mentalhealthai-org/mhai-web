"""Define tasks for answering user messages."""

from __future__ import annotations

import warnings

from typing import Any

from celery import shared_task
from mhailib.messages.ai_answer import ask_ai

from my_diary.models import MhaiDiary


@shared_task
def process_chat_answer(message_id: int, user_id: int) -> None:
    """
    Process and enrich a chat message with additional analysis information.

    This task retrieves the necessary data for the specified chat message ID,
    including MhaiDiary details and related evaluation data, and performs
    the required processing.

    Parameters
    ----------
    message_id : int
        The ID of the MhaiDiary message to process.
    """
    try:
        # Retrieve the MhaiDiary message instance by ID
        chat_message = MhaiDiary.objects.get(id=message_id)

        answer = ask_ai(prompt=chat_message.prompt, user_id=user_id)
        chat_message.response = answer
        chat_message.save()

    except MhaiDiary.DoesNotExist as e:
        # Log error if the MhaiDiary message with given ID does not exist
        warnings.warn(
            f"Error: MhaiDiary message with id {message_id} does not exist.",
            stacklevel=2,
        )
        raise e
    except Exception as e:
        warnings.warn(f"Error: {e}", stacklevel=2)
        chat_message_fallback = MhaiDiary.objects.filter(id=message_id)
        if chat_message_fallback:
            chat_message.status = "error"
            chat_message.save()
        raise e


@shared_task
def finish_answering(result: list[Any], message_id: int) -> None:
    try:
        # Retrieve the MhaiDiary message instance by ID
        chat_message = MhaiDiary.objects.get(id=message_id)
        chat_message.status = "completed"
        chat_message.save()

    except MhaiDiary.DoesNotExist as e:
        # Log error if the MhaiDiary message with given ID does not exist
        warnings.warn(
            f"Error: MhaiDiary message with id {message_id} does not exist.",
            stacklevel=2,
        )
        raise e
    except Exception as e:
        warnings.warn(f"Error: {e}", stacklevel=2)
        chat_message_fallback = MhaiDiary.objects.filter(id=message_id)
        if chat_message_fallback:
            chat_message.status = "error"
            chat_message.save()
        raise e
