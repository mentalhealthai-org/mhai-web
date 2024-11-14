"""Define tasks for answering user messages."""

from __future__ import annotations

from typing import Any

from celery import shared_task

from mhai_chat.api.serializers import (
    MhaiChatEvalEmotionsSerializer,
    MhaiChatEvalMentBertSerializer,
    MhaiChatEvalPsychBertSerializer,
    MhaiChatSerializer,
)
from mhai_chat.models import MhaiChat


@shared_task
def process_chat_answer(message_id: int) -> None:
    """
    Task to process and enrich a chat message with additional analysis information.

    This task retrieves the necessary data for the specified chat message ID,
    including MhaiChat details and related evaluation data, and performs
    the required processing.

    Parameters
    ----------
    message_id : int
        The ID of the MhaiChat message to process.
    """
    try:
        # Retrieve the MhaiChat message instance by ID
        chat_message = MhaiChat.objects.get(id=message_id)

        # Serialize the main chat message
        chat_data = MhaiChatSerializer(chat_message).data

        # Collect associated evaluation data
        emotions_data = (
            MhaiChatEvalEmotionsSerializer(
                chat_message.mhaichatevalemotions
            ).data
            if hasattr(chat_message, "mhaichatevalemotions")
            else {}
        )
        mentbert_data = (
            MhaiChatEvalMentBertSerializer(
                chat_message.mhaichatevalmentbert
            ).data
            if hasattr(chat_message, "mhaichatevalmentbert")
            else {}
        )
        psychbert_data = (
            MhaiChatEvalPsychBertSerializer(
                chat_message.mhaichatevalpsychbert
            ).data
            if hasattr(chat_message, "mhaichatevalpsychbert")
            else {}
        )

        # Compile all data for processing
        enriched_data = {
            "chat": chat_data,
            "emotions": emotions_data,
            "mentbert": mentbert_data,
            "psychbert": psychbert_data,
        }

        # Here, you would add code to further process or handle `enriched_data`
        # For example, you might send it to another service, perform analysis,
        # or log the results for later use.
        # Example placeholder for handling:
        handle_enriched_data(enriched_data)

    except MhaiChat.DoesNotExist:
        # Log error if the MhaiChat message with given ID does not exist
        print(f"Error: MhaiChat message with id {message_id} does not exist.")


def handle_enriched_data(data: dict[str, Any]) -> None:
    """
    Placeholder function to handle enriched data.

    Parameters
    ----------
    data : dict
        The enriched data containing the chat and related evaluation information.
    """
    # Placeholder for further handling of `data`
    # Example: Log the data, send it to an API, or store it for analytics
    print("Enriched data processed:", data)
