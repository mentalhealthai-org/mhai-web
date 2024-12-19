"""Set of functions for handling data from patient."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

import pandas as pd

from asgiref.sync import sync_to_async
from mhai_chat.models import (
    MhaiChat,
    MhaiChatEvalEmotions,
    MhaiChatEvalMentBert,
    MhaiChatEvalPsychBert,
)
from typeguard import typechecked

if TYPE_CHECKING:
    from datetime import datetime


@typechecked
async def fetch_model_data(
    model, filters: dict[str, Any] = {}
) -> pd.DataFrame:
    """Fetch data from a Django and convert it to a DataFrame."""

    @sync_to_async
    def query_model():
        return pd.DataFrame.from_records(
            model.objects.filter(**filters).values()
        )

    return await query_model()


@typechecked
async def prepare_user_data() -> pd.DataFrame:
    """Prepare user data by merging relevant model data."""
    df_chat = await fetch_model_data(MhaiChat, filters={"status": "completed"})
    df_emotions = await fetch_model_data(MhaiChatEvalEmotions)
    df_mentbert = await fetch_model_data(MhaiChatEvalMentBert)
    df_psychbert = await fetch_model_data(MhaiChatEvalPsychBert)

    # rename columns
    skip_renaming = ("id", "mhai_chat_id")
    df_emotions.rename(
        columns={
            c: f"emotions_{c}"
            for c in df_emotions.columns
            if c not in skip_renaming
        },
        inplace=True,
    )
    df_mentbert.rename(
        columns={
            c: f"mentbert_{c}"
            for c in df_mentbert.columns
            if c not in skip_renaming
        },
        inplace=True,
    )
    df_psychbert.rename(
        columns={
            c: f"psychbert_{c}"
            for c in df_psychbert.columns
            if c not in skip_renaming
        },
        inplace=True,
    )

    # Merge dataframes on the common key `id`
    df_complete = df_chat.merge(
        df_emotions,
        left_on="id",
        right_on="mhai_chat_id",
        how="left",
        suffixes=("", "_y"),
    )
    df_complete = df_complete.merge(
        df_mentbert,
        left_on="id",
        right_on="mhai_chat_id",
        how="left",
        suffixes=("", "_y"),
    )
    df_complete = df_complete.merge(
        df_psychbert,
        left_on="id",
        right_on="mhai_chat_id",
        how="left",
        suffixes=("", "_y"),
    )

    df_complete = df_complete[df_complete["prompt"].notna()]
    import joblib

    joblib.dump(
        df_complete, "~/dev/mentalhealthai-org/notebook/data/result.pkl"
    )
    return df_complete


@typechecked
def process_emotions(df_complete: pd.DataFrame) -> pd.DataFrame:
    """Add emotion labels to the DataFrame."""
    emotions = [
        "emotions_fear",
        "emotions_sadness",
        "emotions_neutral",
        "emotions_joy",
        "emotions_surprise",
        "emotions_anger",
        "emotions_disgust",
    ]
    df_complete["emotion_label"] = df_complete[emotions].idxmax(axis=1)
    return df_complete


@typechecked
def filter_data_by_date(
    df_complete: pd.DataFrame, start_date: datetime | None = None
) -> pd.DataFrame:
    """Filter the DataFrame based on a date range."""
    if start_date:
        df_complete = df_complete[
            df_complete["prompt_timestamp"] >= start_date
        ]
    return df_complete


@typechecked
def get_most_frequent_labels(
    df_complete: pd.DataFrame, category: str, top: int
) -> pd.DataFrame:
    """Retrieve the most frequent labels for a specific category."""
    col_name = f"{category.lower()}_label"
    return (
        df_complete[col_name]
        .value_counts()
        .head(top)
        .reset_index()
        .rename(columns={col_name: "label"})
    )
