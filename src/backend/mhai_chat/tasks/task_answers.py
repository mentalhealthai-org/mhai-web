"""Define tasks for answering user messages."""

from __future__ import annotations

from celery import shared_task
from mhailib.messages.ai_answer import ask_ai

from mhai_chat.models import MhaiChat


@shared_task
def process_chat_answer(message_id: int, user_id: int) -> None:
    """
    Process and enrich a chat message with additional analysis information.

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

        answer = ask_ai(prompt=chat_message.user_input, user_id=user_id)
        chat_message.ai_response = answer
        chat_message.save()

    except MhaiChat.DoesNotExist:
        # Log error if the MhaiChat message with given ID does not exist
        print(f"Error: MhaiChat message with id {message_id} does not exist.")
        chat_message.status = "error"
        chat_message.save()
