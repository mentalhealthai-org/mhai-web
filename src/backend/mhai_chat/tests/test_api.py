import pytest

from django.urls import reverse
from rest_framework import status

from mhai_chat.models import MhaiChat


@pytest.mark.django_db
def test_create_chat_message(auth_client, user):
    """
    Test creating a chat message for an authenticated user.
    """
    payload = {"prompt": "Hello, AI!"}
    url = reverse("mhai-chat-list")
    response = auth_client.post(url, payload, format="json")

    assert response.status_code == status.HTTP_201_CREATED
    assert MhaiChat.objects.filter(user=user).count() == 1

    chat_message = MhaiChat.objects.get(user=user)
    assert chat_message.prompt == "Hello, AI!"
    # note: tasks celery is running in sequence
    assert chat_message.status == "completed"
    assert chat_message.response != ""


@pytest.mark.django_db
def test_get_chat_messages(auth_client, user):
    """
    Test retrieving chat messages for the authenticated user.
    """
    # Create some chat messages
    MhaiChat.objects.create(
        user=user, prompt="First message", status="completed"
    )
    MhaiChat.objects.create(
        user=user, prompt="Second message", status="completed"
    )

    url = reverse("mhai-chat-list")
    response = auth_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 2  # noqa: PLR2004


@pytest.mark.django_db
def test_filter_chat_messages_since_id(auth_client, user):
    """
    Test filtering chat messages using since_id.
    """
    message1 = MhaiChat.objects.create(
        user=user, prompt="First message", status="completed"
    )
    message2 = MhaiChat.objects.create(
        user=user, prompt="Second message", status="completed"
    )

    url = reverse("mhai-chat-list")
    response = auth_client.get(f"{url}?since_id={message1.id}")

    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 1

    last_message = response.json()[0]
    assert last_message["prompt"] == message2.prompt
