# my_diary/tasks/evaluations.py

from __future__ import annotations

import logging

from celery import shared_task
from mhailib.messages.evaluations import (
    eval_emotions,
    eval_mentbert,
    eval_psychbert,
)

from my_diary.models import (
    MhaiDiaryEvalEmotions,
    MhaiDiaryEvalMentBert,
    MhaiDiaryEvalPsychBert,
    MyDiary,
)

logger = logging.getLogger(__name__)


def clean_name(
    data: dict[str, float],
    rename: dict[str, str] = {},  # noqa: B006
) -> dict[str, float]:
    """Clean the key attribute to be used as a field."""
    return {rename.get(k, k).replace("-", "_"): v for k, v in data.items()}


@shared_task
def evaluate_emotions(message_id: int) -> None:
    """
    Task to process emotion analysis for a given chat message.

    Parameters
    ----------
    message_id : int
        The ID of the MyDiary message to analyze emotions.
    """
    try:
        chat_message = MyDiary.objects.get(id=message_id)

        # Example placeholder for the actual emotion analysis logic
        emotions_data = clean_name(eval_emotions(chat_message.prompt))

        # Save the analysis results to MhaiDiaryEvalEmotions
        MhaiDiaryEvalEmotions.objects.update_or_create(
            my_diary=chat_message,
            defaults=emotions_data,
        )

    except MyDiary.DoesNotExist as e:
        logger.error(
            f"Error: MyDiary message with id {message_id} does not exist."
        )
        raise e
    except Exception as e:
        logger.error(f"Error: {e}")
        chat_message_fallback = MyDiary.objects.filter(id=message_id)
        if chat_message_fallback:
            chat_message.status = "error"
            chat_message.save()
        raise e


@shared_task
def evaluate_mentbert(message_id: int) -> None:
    """
    Task to process MentBERT analysis for a given chat message.

    Parameters
    ----------
    message_id : int
        The ID of the MyDiary message to analyze with MentBERT.
    """
    try:
        chat_message = MyDiary.objects.get(id=message_id)

        # Example placeholder for the actual MentBERT analysis logic
        mentbert_data = clean_name(eval_mentbert(chat_message.prompt))

        # Save the analysis results to MhaiDiaryEvalMentBert
        MhaiDiaryEvalMentBert.objects.update_or_create(
            my_diary=chat_message,
            defaults=mentbert_data,
        )

    except MyDiary.DoesNotExist as e:
        logger.error(
            f"Error: MyDiary message with id {message_id} does not exist."
        )
        raise e
    except Exception as e:
        logger.error(f"Error: {e}")
        chat_message_fallback = MyDiary.objects.filter(id=message_id)
        if chat_message_fallback:
            chat_message.status = "error"
            chat_message.save()
        raise e


@shared_task
def evaluate_psychbert(message_id: int) -> None:
    """
    Task to process PsychBERT analysis for a given chat message.

    Parameters
    ----------
    message_id : int
        The ID of the MyDiary message to analyze with PsychBERT.
    """
    try:
        chat_message = MyDiary.objects.get(id=message_id)

        # Example placeholder for the actual PsychBERT analysis logic
        psychbert_data = clean_name(
            eval_psychbert(chat_message.prompt),
            {"negative": "unrelated"},
        )

        # Save the analysis results to MhaiDiaryEvalPsychBert
        MhaiDiaryEvalPsychBert.objects.update_or_create(
            my_diary=chat_message,
            defaults=psychbert_data,
        )

    except MyDiary.DoesNotExist as e:
        logger.error(
            f"Error: MyDiary message with id {message_id} does not exist."
        )
        raise e
    except Exception as e:
        logger.error(f"Error: {e}")
        chat_message_fallback = MyDiary.objects.filter(id=message_id)
        if chat_message_fallback:
            chat_message.status = "error"
            chat_message.save()
        raise e
