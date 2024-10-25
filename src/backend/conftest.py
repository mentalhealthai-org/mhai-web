"""Test configuration module."""

import pytest

from django.contrib.auth import get_user_model
from mhai_web.users.models import User as UserClass

User = get_user_model()


@pytest.fixture
def user() -> UserClass:
    """Fixture to create a test User instance."""
    return User.objects.create_user(
        email="test@mymhai.com",
        password="password",  # noqa: S106
    )
