"""Mhai Chat URLs."""

from __future__ import annotations

from django.urls import path

from mhai_chat import views

urlpatterns = [
    path("mhai-chat/", views.MhaiChatView.as_view(), name="mhai-chat"),
]
