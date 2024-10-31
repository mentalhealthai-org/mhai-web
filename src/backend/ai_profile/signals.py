"""Define the signals linked to the user profile."""

from __future__ import annotations

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from ai_profile.models import AIProfile


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_ai_profile(sender, instance, created, **kwargs):
    """Creates a AIProfile automatically when a new User is created."""
    if created:
        AIProfile.objects.create(user=instance, age=0)
