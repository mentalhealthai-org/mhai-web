from typing import ClassVar

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from simple_history.models import HistoricalRecords

from .managers import UserManager


class User(AbstractUser):
    """
    Custom user model for Mhai-Web with extended fields and history tracking.

    This model includes modifications for supporting history tracking using
    Django Simple History's `HistoricalRecords`, allowing the capture of each
    instance's history, such as changes to name or email, over time.
    """

    name = models.CharField(_("Name of User"), blank=True, max_length=255)
    first_name = None  # type: ignore[assignment]
    last_name = None  # type: ignore[assignment]
    email = models.EmailField(_("email address"), unique=True)
    username = None  # type: ignore[assignment]

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects: ClassVar[UserManager] = UserManager()

    history = HistoricalRecords()

    def get_absolute_url(self) -> str:
        """
        Returns the URL for this user's detail view.

        Returns
        -------
        str
            URL for user's detail.
        """
        return reverse("users:detail", kwargs={"pk": self.id})
