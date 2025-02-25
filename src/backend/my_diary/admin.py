"""Admin module for my_diary."""

from django.contrib import admin

from my_diary.models import (
    MhaiDiary,
    MhaiDiaryEvalEmotions,
    MhaiDiaryEvalMentBert,
    MhaiDiaryEvalPsychBert,
)


@admin.register(MhaiDiary)
class MhaiDiaryAdmin(admin.ModelAdmin):
    """Admin configuration for MhaiDiary."""

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


@admin.register(MhaiDiaryEvalEmotions)
class MhaiDiaryEvalEmotionsAdmin(admin.ModelAdmin):
    """Admin configuration for MhaiDiaryEvalEmotions."""

    list_display = ("id", "my_diary", "neutral", "joy", "anger", "fear")
    search_fields = ("my_diary__user__username",)
    ordering = ("my_diary__timestamp_prompt",)


@admin.register(MhaiDiaryEvalMentBert)
class MhaiDiaryEvalMentBertAdmin(admin.ModelAdmin):
    """Admin configuration for MhaiDiaryEvalMentBert."""

    list_display = (
        "id",
        "my_diary",
        "borderline",
        "anxiety",
        "depression",
        "bipolar",
        "ocd",
        "adhd",
    )
    search_fields = ("my_diary__user__username",)
    ordering = ("my_diary__timestamp_prompt",)


@admin.register(MhaiDiaryEvalPsychBert)
class MhaiDiaryEvalPsychBertAdmin(admin.ModelAdmin):
    """Admin configuration for MhaiDiaryEvalPsychBert."""

    list_display = (
        "id",
        "my_diary",
        "unrelated",
        "mental_illnesses",
        "anxiety",
        "depression",
        "loneliness",
    )
    search_fields = ("my_diary__user__username",)
    ordering = ("my_diary__timestamp_prompt",)
