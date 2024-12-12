"""Create the dashboard for patient analysis."""

from __future__ import annotations

from datetime import datetime

import pandas as pd
import plotly.express as px

from asgiref.sync import async_to_sync, sync_to_async
from dash import Input, Output, dcc, html
from dateutil.relativedelta import relativedelta
from django_plotly_dash import DjangoDash
from mhai_chat.models import (
    MhaiChat,
    MhaiChatEvalEmotions,
    MhaiChatEvalMentBert,
    MhaiChatEvalPsychBert,
)


async def fetch_model_data(model) -> pd.DataFrame:
    """Fetch data from a Django model asynchronously and convert it to a DataFrame."""

    @sync_to_async
    def query_model():
        return pd.DataFrame.from_records(model.objects.all().values())

    return await query_model()


async def prepare_user_data() -> pd.DataFrame:
    """Prepare user data by merging relevant model data."""
    df_chat = await fetch_model_data(MhaiChat)
    df_emotions = await fetch_model_data(MhaiChatEvalEmotions)
    df_mentbert = await fetch_model_data(MhaiChatEvalMentBert)
    df_psychbert = await fetch_model_data(MhaiChatEvalPsychBert)

    # Merge dataframes on the common key `id`
    df = df_chat.merge(
        df_emotions, left_on="id", right_on="mhai_chat_id", how="left"
    )
    df = df.merge(
        df_mentbert, left_on="id", right_on="mhai_chat_id", how="left"
    )
    df = df.merge(
        df_psychbert, left_on="id", right_on="mhai_chat_id", how="left"
    )

    # Ensure only valid rows with user input
    return df[df["user_prompt"].notnull()]


def process_emotions(df: pd.DataFrame) -> pd.DataFrame:
    """Add emotion labels to the DataFrame."""
    emotions = [
        "fear",
        "sadness",
        "neutral",
        "joy",
        "surprise",
        "anger",
        "disgust",
    ]
    df["emotion_label"] = df[emotions].idxmax(axis=1)
    return df


def filter_data_by_date(
    df: pd.DataFrame, start_date: datetime | None = None
) -> pd.DataFrame:
    """Filter the DataFrame based on a date range."""
    if start_date:
        df = df[df["timestamp_prompt"] >= start_date]
    return df


def get_frequent_labels(
    df: pd.DataFrame, category: str, top: int
) -> pd.DataFrame:
    """Retrieve the most frequent labels for a specific category."""
    col_name = f"{category.lower()}_label"
    return (
        df[col_name]
        .value_counts()
        .head(top)
        .reset_index()
        .rename(columns={col_name: "count", "index": "label"})
    )


def create_bar_chart(df: pd.DataFrame, category: str, top: int) -> dcc.Graph:
    """Create a bar chart for the top labels in a category."""
    frequent_labels = get_frequent_labels(df, category, top)
    fig = px.bar(frequent_labels, x="label", y="count")
    fig.update_layout(height=300, margin=dict(l=20, r=20, t=40, b=20))
    return dcc.Graph(figure=fig)


def create_timeseries_chart(
    df: pd.DataFrame, category: str, top: int
) -> dcc.Graph:
    """Create a time series chart for the top labels in a category."""
    col_name = f"{category.lower()}_label"
    top_labels = get_frequent_labels(df, category, top)["label"].tolist()
    df_ts = (
        df[df[col_name].isin(top_labels)]
        .groupby(["timestamp_prompt", col_name])
        .size()
        .reset_index(name="count")
    )
    fig = px.line(df_ts, x="timestamp_prompt", y="count", color=col_name)
    fig.update_layout(height=300, margin=dict(l=20, r=20, t=40, b=20))
    return dcc.Graph(figure=fig)


# Initialize Dash App
external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]
app = DjangoDash(
    "DashboardPatientView", external_stylesheets=external_stylesheets
)

# Layout Definition
# Updated Layout
app.layout = html.Div(
    children=[
        html.Div(
            children=[
                html.Label("Number of Top Items"),
                dcc.Input(
                    id="top-input", type="number", value=3, min=1, step=1
                ),
                html.Label("Time Period"),
                dcc.Dropdown(
                    id="period-dropdown",
                    options=[
                        {"label": "1 Month", "value": "1m"},
                        {"label": "3 Months", "value": "3m"},
                        {"label": "6 Months", "value": "6m"},
                        {"label": "1 Year", "value": "1y"},
                        {"label": "All Time", "value": "max"},
                    ],
                    value="max",
                ),
                html.Label("Number of Records"),
                dcc.Input(id="txt-records", disabled=True),
            ]
        ),
        html.Div(
            children=[
                html.H2("Mental"),
                html.Div(id="div-mental"),
                html.Div(id="div-mental-ts"),
            ]
        ),
        html.Div(
            children=[
                html.H2("Psychological"),
                html.Div(id="div-psychological"),
                html.Div(id="div-psychological-ts"),
            ]
        ),
        html.Div(
            children=[
                html.H2("Emotional"),
                html.Div(id="div-emotional"),
                html.Div(id="div-emotional-ts"),
            ]
        ),
    ]
)


# Updated Callback
@app.callback(
    Output("div-mental", "children"),
    Output("div-psychological", "children"),
    Output("div-emotional", "children"),
    Output("div-mental-ts", "children"),
    Output("div-psychological-ts", "children"),
    Output("div-emotional-ts", "children"),
    Output("txt-records", "value"),
    Input("top-input", "value"),
    Input("period-dropdown", "value"),
)
def update_dashboard(n_top: int, period: str):
    df = async_to_sync(prepare_user_data)()
    df = process_emotions(df)

    # Date range filtering
    if period != "max":
        months = int(period[:-1])
        start_date = datetime.now() - relativedelta(months=months)
        df = filter_data_by_date(df, start_date=start_date)

    mental_bar = create_bar_chart(df, "Mental", n_top)
    psych_bar = create_bar_chart(df, "Psychological", n_top)
    emotion_bar = create_bar_chart(df, "Emotional", n_top)

    # For time series
    mental_ts = create_timeseries_chart(df, "Mental", n_top)
    psych_ts = create_timeseries_chart(df, "Psychological", n_top)
    emotion_ts = create_timeseries_chart(df, "Emotional", n_top)

    n_records = len(df)

    return (
        mental_bar,
        psych_bar,
        emotion_bar,
        mental_ts,
        psych_ts,
        emotion_ts,
        n_records,
    )
