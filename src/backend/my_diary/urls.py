"""Mhai Chat URLs."""

from __future__ import annotations

from django.urls import path

from my_diary import views

urlpatterns = [
    path("mhai-chat/", views.MhaiDiaryView.as_view(), name="mhai-chat"),
]
