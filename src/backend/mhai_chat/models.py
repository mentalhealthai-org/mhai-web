from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class ChatRoom(models.Model):
    """
    Model representing a chat room.
    """

    name = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Message(models.Model):
    """
    Model representing a message within a chat room.
    """

    chat_room = models.ForeignKey(
        ChatRoom, related_name="messages", on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        User, null=True, on_delete=models.SET_NULL
    )  # Null for AI responses
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    message_type = models.CharField(
        max_length=10, choices=[("USER", "User"), ("AI", "AI")], default="USER"
    )

    class Meta:
        ordering = ["-timestamp"]

    def __str__(self):
        return f"Message from {
            self.user or 'AI'
            } in {self.chat_room.name} at {self.timestamp}"
