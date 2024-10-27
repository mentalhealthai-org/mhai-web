"""
Management utility to create superusers.
This overrides the default django's `createsuperuser` command.
"""

from typing import Any

from allauth.account.models import EmailAddress
from django.contrib.auth import get_user_model
from django.contrib.auth.management.commands.createsuperuser import (
    Command as SuperUserCommand,
)


class Command(SuperUserCommand):
    """ "Django Command class which inherits from createsuperuser Command"""

    def handle(self, *args: Any, **options: Any) -> None:
        """
        Handle the creation of a superuser and activate the account.

        This method extends the default Django `createsuperuser` command
        by automatically activating the created superuser account using
        the allauth `EmailAddress` model.

        Parameters
        ----------
        *args : Any
            Variable length argument list.
        **options : Any
            Arbitrary keyword arguments.

        Notes
        -----
        The method first calls the superclass handle method to create the
        superuser. Then, it attempts to fetch the created user based on the
        provided email and creates an associated `EmailAddress` instance,
        marking it as verified and primary. If the superuser is not created
        (e.g., due to invalid input), the method exits without further action.
        """
        super().handle(*args, **options)

        User = get_user_model()  # noqa: N806

        # fetch the created superuser
        created_user = User.objects.get(email=options["email"])

        # activate the created superuser account
        EmailAddress.objects.create(
            user=created_user,
            email=created_user.email,
            primary=True,
            verified=True,
        )
