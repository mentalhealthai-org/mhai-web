from datetime import datetime, timedelta

import pandas as pd
import pytest

from django.utils.timezone import now
from mhai_chat.models import (
    MhaiChat,
    MhaiChatEvalEmotions,
    MhaiChatEvalMentBert,
    MhaiChatEvalPsychBert,
)
from mhai_web.users.models import User

from dashboards.libs.data.patient import (
    filter_data_by_date,
    get_most_frequent_labels,
    prepare_user_data,
    process_emotions,
)


@pytest.fixture
def create_test_data(db, user: User):
    """Fixture to create initial test data for the models."""
    user_id = user.id
    chat1 = MhaiChat.objects.create(
        user_id=user_id,
        prompt="How are you?",
        response="I'm fine.",
        status="completed",
        prompt_timestamp=now() - timedelta(days=3),
    )
    chat2 = MhaiChat.objects.create(
        user_id=user_id,
        prompt="Tell me a joke.",
        response="Why did the chicken cross the road?",
        status="completed",
        prompt_timestamp=now() - timedelta(days=2),
    )
    chat3 = MhaiChat.objects.create(
        user_id=user_id,
        prompt="What is AI?",
        response="AI stands for artificial intelligence.",
        status="completed",
        prompt_timestamp=now() - timedelta(days=1),
    )

    MhaiChatEvalEmotions.objects.create(
        mhai_chat=chat1,
        fear=0.1,
        sadness=0.2,
        neutral=0.5,
        joy=0.2,
        surprise=0.0,
        anger=0.0,
        disgust=0.0,
    )
    MhaiChatEvalEmotions.objects.create(
        mhai_chat=chat2,
        fear=0.0,
        sadness=0.0,
        neutral=0.3,
        joy=0.6,
        surprise=0.1,
        anger=0.0,
        disgust=0.0,
    )
    MhaiChatEvalEmotions.objects.create(
        mhai_chat=chat3,
        fear=0.2,
        sadness=0.1,
        neutral=0.3,
        joy=0.3,
        surprise=0.0,
        anger=0.1,
        disgust=0.0,
    )

    MhaiChatEvalMentBert.objects.create(
        mhai_chat=chat1,
        borderline=0.1,
        anxiety=0.2,
        depression=0.3,
        bipolar=0.0,
        ocd=0.4,
        adhd=0.1,
        schizophrenia=0.2,
        asperger=0.0,
        ptsd=0.2,
    )
    MhaiChatEvalMentBert.objects.create(
        mhai_chat=chat2,
        borderline=0.0,
        anxiety=0.1,
        depression=0.2,
        bipolar=0.1,
        ocd=0.3,
        adhd=0.4,
        schizophrenia=0.1,
        asperger=0.2,
        ptsd=0.1,
    )
    MhaiChatEvalMentBert.objects.create(
        mhai_chat=chat3,
        borderline=0.2,
        anxiety=0.0,
        depression=0.1,
        bipolar=0.3,
        ocd=0.2,
        adhd=0.0,
        schizophrenia=0.4,
        asperger=0.1,
        ptsd=0.3,
    )

    MhaiChatEvalPsychBert.objects.create(
        mhai_chat=chat1,
        unrelated=0.3,
        mental_illnesses=0.2,
        anxiety=0.1,
        depression=0.2,
        social_anxiety=0.2,
        loneliness=0.1,
    )
    MhaiChatEvalPsychBert.objects.create(
        mhai_chat=chat2,
        unrelated=0.2,
        mental_illnesses=0.1,
        anxiety=0.0,
        depression=0.3,
        social_anxiety=0.4,
        loneliness=0.2,
    )
    MhaiChatEvalPsychBert.objects.create(
        mhai_chat=chat3,
        unrelated=0.1,
        mental_illnesses=0.3,
        anxiety=0.2,
        depression=0.1,
        social_anxiety=0.0,
        loneliness=0.4,
    )


@pytest.mark.django_db
async def test_prepare_user_data(create_test_data):
    """Test prepare_user_data function."""
    df = await prepare_user_data()
    assert isinstance(df, pd.DataFrame)
    assert df.shape[0] == 3
    assert "user_prompt" in df.columns
    assert "emotions_joy" in df.columns


def test_process_emotions(create_test_data):
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


def test_filter_data_by_date(create_test_data):
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


def test_get_most_frequent_labels(create_test_data):
    """Test get_most_frequent_labels function."""
    df = pd.DataFrame(
        {"emotions_label": ["neutral", "joy", "neutral", "joy", "joy"]}
    )
    frequent_labels = get_most_frequent_labels(df, "emotions", top=2)
    assert frequent_labels.iloc[0]["label"] == "joy"
    assert frequent_labels.iloc[1]["label"] == "neutral"
