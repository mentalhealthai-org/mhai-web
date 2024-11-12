""""""

from __future__ import annotations

from celery import shared_task
from django.utils import timezone

from mhai_chat.models import Message


@shared_task
def generate_ai_response(message_id):
    message = Message.objects.get(id=message_id)
    # Call your AI model or external API here
    ai_response = "This is an AI-generated response."
    Message.objects.create(
        chat_room=message.chat_room,
        user=None,  # AI as the responder, no actual user
        content=ai_response,
        timestamp=timezone.now(),
        message_type="AI",
    )
