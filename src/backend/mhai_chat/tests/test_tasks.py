import pytest

from mhai_chat.models import MhaiChat
from mhai_chat.tasks.task_answers import process_chat_answer


@pytest.mark.django_db
def test_process_chat_answer_success(user):
    """
    Test the process_chat_answer task.

    Check the result when the chat message exists and processing succeeds.
    """
    chat_message = MhaiChat.objects.create(
        user=user, user_input="Hello, AI!", ai_response="", status="started"
    )

    process_chat_answer(message_id=chat_message.id, user_id=user.id)

    chat_message.refresh_from_db()
    assert chat_message.ai_response != ""
    assert chat_message.status == "started"


@pytest.mark.django_db
def test_process_chat_answer_message_does_not_exist(user):
    """
    Test the process_chat_answer task when the chat message does not exist.
    """
    invalid_message_id = 999  # Assume this ID doesn't exist
    process_chat_answer(message_id=invalid_message_id, user_id=user.id)

    assert MhaiChat.objects.filter(id=invalid_message_id).count() == 0
