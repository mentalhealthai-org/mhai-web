import pytest

from simple_history.utils import update_change_reason

from mhai_web.users.models import User


@pytest.mark.django_db
class TestUserHistory:
    def test_creation_history_reason(self, caplog):
        """
        Test that creating a User instance records "User created" as the change reason.
        """
        with caplog.at_level("INFO"):
            user = User.objects.create(email="example@example.com", name="Example User")
            history = user.history.first()

            assert history.history_change_reason == "User created"
            assert "User example@example.com was last changed on" in caplog.text

    def test_update_history_reason(self, caplog):
        """
        Test that updating an existing User instance records.
        """
        user = User.objects.create(email="example@example.com", name="Example User")

        user.name = "Updated User"
        user.save()

        update_change_reason(user, "User updated")

        last_history = user.history.first()

        assert last_history.history_change_reason == "User updated"
        assert "User example@example.com was last changed on" in caplog.text

    def test_logging_on_change(self, caplog):
        """
        Test that logging output appears when a User instance is created or updated.
        """
        with caplog.at_level("INFO"):
            user = User.objects.create(email="example@example.com", name="Example User")
            assert "User example@example.com was last changed on" in caplog.text

        with caplog.at_level("INFO"):
            user.name = "Updated User"
            user.save()
            update_change_reason(user, "User updated")
            assert "User example@example.com was last changed on" in caplog.text
