from rest_framework import serializers

from .models import ChatRoom, Message


class ChatRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatRoom
        fields = [
            "id",
            "name",
            "created_at",
        ]  # Use 'name' field instead of 'room_name'


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = [
            "id",
            "chat_room",
            "user",
            "content",
            "timestamp",
        ]  # Use 'user' instead of 'sender'
