import pytest

from simple_history.utils import update_change_reason

from mhai_web.users.models import User


@pytest.mark.django_db
class TestUserHistory:
    def test_creation_history_reason(self, caplog):
        """Test the User creation with history."""
        with caplog.at_level("INFO"):
            user = User.objects.create(
                email="example@example.com", name="Example User"
            )
            history = user.history.first()

            assert history.history_change_reason == "User created"
            assert (
                "User example@example.com was last changed on" in caplog.text
            )

    def test_update_history_reason(self, caplog):
        """Test User updating with history."""
        user = User.objects.create(
            email="example@example.com", name="Example User"
        )

        user.name = "Updated User"
        user.save()

        update_change_reason(user, "User updated")

        last_history = user.history.first()

        assert last_history.history_change_reason == "User updated"
        assert "User example@example.com was last changed on" in caplog.text

    def test_logging_on_change(self, caplog):
        """Test logging output."""

        with caplog.at_level("INFO"):
            user = User.objects.create(
                email="example@example.com", name="Example User"
            )
            assert (
                "User example@example.com was last changed on" in caplog.text
            )

        with caplog.at_level("INFO"):
            user.name = "Updated User"
            user.save()
            update_change_reason(user, "User updated")
            assert (
                "User example@example.com was last changed on" in caplog.text
            )
