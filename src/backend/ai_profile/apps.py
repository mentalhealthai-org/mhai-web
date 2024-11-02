"""User Profile app."""

from django.apps import AppConfig


class AIProfileConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "ai_profile"

    def ready(self):
        # Import signals to ensure they are registered
        pass
