"""Admin module for mhai_chat."""

from django.contrib import admin

from mhai_chat.models import (
    MhaiChat,
    MhaiChatEvalEmotions,
    MhaiChatEvalMentBert,
    MhaiChatEvalPsychBert,
)


@admin.register(MhaiChat)
class MhaiChatAdmin(admin.ModelAdmin):
    """Admin configuration for MhaiChat."""

    list_display = (
        "id",
        "user",
        "prompt_timestamp",
        "response_timestamp",
        "status",
    )
    list_filter = ("status", "prompt_timestamp", "response_timestamp")
    search_fields = ("user__username", "user_input", "response")
    ordering = ("-prompt_timestamp",)


@admin.register(MhaiChatEvalEmotions)
class MhaiChatEvalEmotionsAdmin(admin.ModelAdmin):
    """Admin configuration for MhaiChatEvalEmotions."""

    list_display = ("id", "mhai_chat", "neutral", "joy", "anger", "fear")
    search_fields = ("mhai_chat__user__username",)
    ordering = ("mhai_chat__timestamp_prompt",)


@admin.register(MhaiChatEvalMentBert)
class MhaiChatEvalMentBertAdmin(admin.ModelAdmin):
    """Admin configuration for MhaiChatEvalMentBert."""

    list_display = (
        "id",
        "mhai_chat",
        "borderline",
        "anxiety",
        "depression",
        "bipolar",
        "ocd",
        "adhd",
    )
    search_fields = ("mhai_chat__user__username",)
    ordering = ("mhai_chat__timestamp_prompt",)


@admin.register(MhaiChatEvalPsychBert)
class MhaiChatEvalPsychBertAdmin(admin.ModelAdmin):
    """Admin configuration for MhaiChatEvalPsychBert."""

    list_display = (
        "id",
        "mhai_chat",
        "unrelated",
        "mental_illnesses",
        "anxiety",
        "depression",
        "loneliness",
    )
    search_fields = ("mhai_chat__user__username",)
    ordering = ("mhai_chat__timestamp_prompt",)
