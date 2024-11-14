# mhai_chat/tasks/evaluations.py

from __future__ import annotations

from celery import shared_task
from mhailib.messages.evaluations import (
    eval_emotions,
    eval_mentbert,
    eval_psychbert,
)

from mhai_chat.models import (
    MhaiChat,
    MhaiChatEvalEmotions,
    MhaiChatEvalMentBert,
    MhaiChatEvalPsychBert,
)


@shared_task
def evaluate_emotions(message_id: int) -> None:
    """
    Task to process emotion analysis for a given chat message.

    Parameters
    ----------
    message_id : int
        The ID of the MhaiChat message to analyze emotions.
    """
    try:
        chat_message = MhaiChat.objects.get(id=message_id)

        # Example placeholder for the actual emotion analysis logic
        emotions_data = eval_emotions(chat_message.user_input)

        # Save the analysis results to MhaiChatEvalEmotions
        MhaiChatEvalEmotions.objects.update_or_create(
            mhai_chat=chat_message,
            defaults=emotions_data,
        )

    except MhaiChat.DoesNotExist:
        print(f"Error: MhaiChat message with id {message_id} does not exist.")


@shared_task
def evaluate_mentbert(message_id: int) -> None:
    """
    Task to process MentBERT analysis for a given chat message.

    Parameters
    ----------
    message_id : int
        The ID of the MhaiChat message to analyze with MentBERT.
    """
    try:
        chat_message = MhaiChat.objects.get(id=message_id)

        # Example placeholder for the actual MentBERT analysis logic
        mentbert_data = eval_mentbert(chat_message.user_input)

        # Save the analysis results to MhaiChatEvalMentBert
        MhaiChatEvalMentBert.objects.update_or_create(
            mhai_chat=chat_message,
            defaults=mentbert_data,
        )

    except MhaiChat.DoesNotExist:
        print(f"Error: MhaiChat message with id {message_id} does not exist.")


@shared_task
def evaluate_psychbert(message_id: int) -> None:
    """
    Task to process PsychBERT analysis for a given chat message.

    Parameters
    ----------
    message_id : int
        The ID of the MhaiChat message to analyze with PsychBERT.
    """
    try:
        chat_message = MhaiChat.objects.get(id=message_id)

        # Example placeholder for the actual PsychBERT analysis logic
        psychbert_data = eval_psychbert(chat_message.user_input)

        # Save the analysis results to MhaiChatEvalPsychBert
        MhaiChatEvalPsychBert.objects.update_or_create(
            mhai_chat=chat_message,
            defaults=psychbert_data,
        )

    except MhaiChat.DoesNotExist:
        print(f"Error: MhaiChat message with id {message_id} does not exist.")
