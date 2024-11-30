"""User Profile app."""

from django.apps import AppConfig


class AIProfileConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "ai_profile"

    def ready(self):
        import ai_profile.signals  # noqa
