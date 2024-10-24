from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@receiver(post_save, sender=User)
def log_user_update(sender, instance, **kwargs):
    if instance.history.exists():
        last_history = instance.history.first()
        logger.info(f"User {instance.email} was last changed on {last_history.history_date}.")
