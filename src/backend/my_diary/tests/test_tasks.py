import pytest

from ai_profile.models import AIProfile
from mhai_web.users.models import User
from user_profile.models import UserProfile

from my_diary.models import MhaiDiary
from my_diary.tasks.task_answers import process_chat_answer


@pytest.mark.django_db
def test_process_chat_answer_success(
    user: User, ai_profile: AIProfile, user_profile: UserProfile
):
    """
    Test the process_chat_answer task.

    Check the result when the chat message exists and processing succeeds.
    """
    chat_message = MhaiDiary.objects.create(
        user=user, prompt="Hello, AI!", response="", status="started"
    )

    process_chat_answer(message_id=chat_message.id, user_id=user.id)

    chat_message.refresh_from_db()
    assert chat_message.response != ""
    assert chat_message.status == "started"


@pytest.mark.django_db
def test_process_chat_answer_message_does_not_exist(user):
    """
    Test the process_chat_answer task when the chat message does not exist.
    """
    invalid_message_id = 999  # this ID doesn't exist
    with pytest.raises(MhaiDiary.DoesNotExist):
        process_chat_answer(message_id=invalid_message_id, user_id=user.id)
