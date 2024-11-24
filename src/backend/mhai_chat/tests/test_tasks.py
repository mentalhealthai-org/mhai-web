import pytest

from mhai_chat.models import MhaiChat
from mhai_chat.tasks.answers import process_chat_answer


@pytest.mark.django_db
def test_process_chat_answer_success(create_user):
    """
    Test the process_chat_answer task.

    Check the result when the chat message exists and processing succeeds.
    """
    # Arrange: Create a test user and a chat message
    user = create_user()  # Assuming a fixture for creating a test user
    chat_message = MhaiChat.objects.create(
        user=user, user_input="Hello, AI!", ai_response="", status="started"
    )

    # Act: Execute the task
    process_chat_answer(message_id=chat_message.id, user_id=user.id)

    # Assert: Verify the message was processed correctly
    chat_message.refresh_from_db()
    assert chat_message.ai_response != ""  # Ensure AI response was populated
    assert chat_message.status == "started"  # Status remains unchanged


@pytest.mark.django_db
def test_process_chat_answer_message_does_not_exist(create_user):
    """
    Test the process_chat_answer task when the chat message does not exist.
    """
    # Arrange: Create a test user
    user = create_user()

    # Act: Execute the task with a non-existent message ID
    invalid_message_id = 999  # Assume this ID doesn't exist
    process_chat_answer(message_id=invalid_message_id, user_id=user.id)

    # Assert: Verify no message was created or updated
    assert MhaiChat.objects.filter(id=invalid_message_id).count() == 0
