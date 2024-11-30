"""Define the signals linked to the user profile."""

from __future__ import annotations

from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from ai_profile.models import AIProfile

User = get_user_model()


@receiver(post_save, sender=User)
def create_ai_profile(sender, instance, created, **kwargs):
    """Creates a AIProfile automatically when a new User is created."""
    if created:
        AIProfile.objects.create(user=instance, age=0)
