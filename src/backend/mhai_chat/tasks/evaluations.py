"""Task for evaluations."""

from __future__ import annotations

from celery import shared_task

from mhai_chat.models import MhaiChat


@shared_task
def generate_ai_response(message_id: int):
    """Generate the AI response."""
    MhaiChat.objects.get(id=message_id)
