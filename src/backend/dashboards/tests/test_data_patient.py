from datetime import datetime, timedelta

import pandas as pd
import pytest

from dashboards.libs.data.patient import (
    filter_data_by_date,
    get_most_frequent_labels,
    prepare_user_data,
    process_emotions,
)


@pytest.mark.django_db
async def test_prepare_user_data(chat_data):
    """Test prepare_user_data function."""
    df = await prepare_user_data()
    assert isinstance(df, pd.DataFrame)
    assert df.shape[0] == 3
    assert "user_prompt" in df.columns
    assert "emotions_joy" in df.columns


@pytest.mark.django_db
def test_process_emotions(chat_data):
    """Test process_emotions function."""
    df = pd.DataFrame(
        {
            "emotions_fear": [0.1, 0.0, 0.2],
            "emotions_sadness": [0.2, 0.0, 0.1],
            "emotions_neutral": [0.5, 0.3, 0.3],
            "emotions_joy": [0.2, 0.6, 0.3],
            "emotions_surprise": [0.0, 0.1, 0.0],
            "emotions_anger": [0.0, 0.0, 0.1],
            "emotions_disgust": [0.0, 0.0, 0.0],
        }
    )
    processed_df = process_emotions(df)
    assert "emotion_label" in processed_df.columns
    assert processed_df["emotion_label"].iloc[0] == "emotions_neutral"


@pytest.mark.django_db
def test_filter_data_by_date(chat_data):
    """Test filter_data_by_date function."""
    df = pd.DataFrame(
        {
            "prompt_timestamp": [
                datetime.now() - timedelta(days=1),
                datetime.now() - timedelta(days=3),
                datetime.now() - timedelta(days=5),
            ]
        }
    )
    start_date = datetime.now() - timedelta(days=4)
    filtered_df = filter_data_by_date(df, start_date=start_date)
    assert filtered_df.shape[0] == 2


@pytest.mark.django_db
def test_get_most_frequent_labels(chat_data):
    """Test get_most_frequent_labels function."""
    df = pd.DataFrame(
        {"emotions_label": ["neutral", "joy", "neutral", "joy", "joy"]}
    )
    frequent_labels = get_most_frequent_labels(df, "emotions", top=2)
    assert frequent_labels.iloc[0]["label"] == "joy"
    assert frequent_labels.iloc[1]["label"] == "neutral"
