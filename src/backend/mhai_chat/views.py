from rest_framework import generics
from rest_framework.permissions import AllowAny

from .models import ChatRoom, Message
from .serializers import ChatRoomSerializer, MessageSerializer


class CreateChatRoomView(generics.CreateAPIView):
    queryset = ChatRoom.objects.all()
    serializer_class = ChatRoomSerializer
    permission_classes = [AllowAny]  # No authentication required


class ChatRoomListView(generics.ListAPIView):
    queryset = ChatRoom.objects.all()
    serializer_class = ChatRoomSerializer
    permission_classes = [AllowAny]  # No authentication required


class SendMessageView(generics.CreateAPIView):
    """
    API view to send a message to a chat room.
    """

    serializer_class = MessageSerializer
    permission_classes = [AllowAny]  # No authentication required

    def perform_create(self, serializer):
        serializer.save(
            user=self.request.user
            if self.request.user.is_authenticated
            else None
        )


class GetMessagesView(generics.ListAPIView):
    """
    API view to retrieve messages from a specific chat room.
    """

    serializer_class = MessageSerializer
    permission_classes = [AllowAny]  # No authentication required

    def get_queryset(self):
        room_id = self.kwargs.get("room_id")
        return Message.objects.filter(chat_room_id=room_id).order_by(
            "timestamp"
        )
