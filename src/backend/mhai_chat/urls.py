# mhai_chat/urls.py

from django.urls import path

from .views import (
    ChatRoomListView,
    CreateChatRoomView,
    GetMessagesView,
    SendMessageView,
)

urlpatterns = [
    path("create-room/", CreateChatRoomView.as_view(), name="create-room"),
    path("rooms/", ChatRoomListView.as_view(), name="chat-room-list"),
    path("send-message/", SendMessageView.as_view(), name="send_message"),
    path(
        "messages/<int:room_id>/",
        GetMessagesView.as_view(),
        name="get_messages",
    ),
]
