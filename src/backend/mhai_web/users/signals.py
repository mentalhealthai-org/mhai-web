import logging

from django.db.models.signals import post_save
from django.dispatch import receiver
from simple_history.utils import update_change_reason

from .models import User

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@receiver(post_save, sender=User)
def log_and_set_change_reason(sender, instance, created, **kwargs):
    """
    Logs the latest update and sets a reason for historical records after saving a User instance.

    Parameters
    ----------
    sender : Model
        The model class (User).
    instance : User
        The specific instance of the User model.
    created : bool
        Indicates if this is a new instance creation.
    kwargs : dict
        Additional arguments passed to the signal.
    """
    change_reason = "User created" if created else "User updated"
    update_change_reason(instance, change_reason)

    if instance.history.exists():
        last_history = instance.history.first()
        logger.info(
            f"User {instance.email} was last changed on {last_history.history_date} with reason: {change_reason}."
        )
