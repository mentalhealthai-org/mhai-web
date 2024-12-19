"""Test functions for the patient charts."""

from __future__ import annotations

from datetime import timedelta

import pandas as pd
import pytest

from django.utils.timezone import now

from dashboards.libs.charts.patient import (
    generate_dashboard_data,
    update_dashboard,
)
from dashboards.libs.data.patient import process_emotions


@pytest.fixture
@pytest.mark.django_db
def test_data():
    """Fixture to generate test data."""
    return pd.DataFrame(
        {
            "id": [1, 2, 3],
            "timestamp_prompt": [
                now() - timedelta(days=90),
                now() - timedelta(days=30),
                now() - timedelta(days=10),
            ],
            "prompt": ["Hello", "How are you?", "Tell me a joke"],
            "emotions_fear": [0.1, 0.0, 0.2],
            "emotions_sadness": [0.2, 0.0, 0.1],
            "emotions_neutral": [0.5, 0.3, 0.3],
            "emotions_joy": [0.2, 0.6, 0.3],
            "emotions_surprise": [0.0, 0.1, 0.0],
            "emotions_anger": [0.0, 0.0, 0.1],
            "emotions_disgust": [0.0, 0.0, 0.0],
        }
    )


@pytest.mark.django_db
def test_process_emotions(test_data):
    """Test processing of emotions to add a label column."""
    df = process_emotions(test_data.copy())
    assert "emotion_label" in df.columns
    assert df["emotion_label"].iloc[0] == "emotions_neutral"
    assert df["emotion_label"].iloc[1] == "emotions_joy"


@pytest.mark.django_db
def test_generate_dashboard_data(test_data):
    """Test dashboard data generation with various inputs."""
    # Test All Time Period
    dashboard_data = generate_dashboard_data(test_data, n_top=2, period="max")

    assert dashboard_data["n_records"] == 3
    assert "dcc.Graph" in str(type(dashboard_data["mental_bar"]))
    assert "dcc.Graph" in str(type(dashboard_data["emotion_ts"]))

    # Test 1 Month Period
    dashboard_data = generate_dashboard_data(test_data, n_top=1, period="1m")
    assert dashboard_data["n_records"] == 1

    # Test 3 Months Period
    dashboard_data = generate_dashboard_data(test_data, n_top=3, period="3m")
    assert dashboard_data["n_records"] == 2


@pytest.mark.django_db
def test_update_dashboard(test_data):
    """Test dashboard data generation with various inputs."""
    # Test All Time Period
    dashboard_data = update_dashboard(n_top=2, period="max")
