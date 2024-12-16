"""Create the dashboard for patient analysis."""

from __future__ import annotations

import pandas as pd
import plotly.express as px

from asgiref.sync import async_to_sync
from dash import Input, Output, dcc, html
from dashboards.libs.data.patient import (
    async_to_sync,
    filter_data_by_date,
    get_most_frequent_labels,
    process_emotions,
)
from dateutil.relativedelta import relativedelta
from django.utils.timezone import now
from django_plotly_dash import DjangoDash


def create_bar_chart(
    df_complete: pd.DataFrame, category: str, top: int
) -> dcc.Graph:
    """Create a bar chart for the top labels in a category."""
    frequent_labels = get_most_frequent_labels(df_complete, category, top)
    fig = px.bar(frequent_labels, x="label", y="count")
    fig.update_layout(height=300, margin={"l": 20, "r": 20, "t": 40, "b": 20})
    return dcc.Graph(figure=fig)


def create_timeseries_chart(
    df_complete: pd.DataFrame, category: str, top: int
) -> dcc.Graph:
    """Create a time series chart for the top labels in a category."""
    col_name = f"{category.lower()}_label"
    top_labels = get_most_frequent_labels(df_complete, category, top)[
        "label"
    ].tolist()
    df_ts = (
        df_complete[df_complete[col_name].isin(top_labels)]
        .groupby(["timestamp_prompt", col_name])
        .size()
        .reset_index(name="count")
    )
    fig = px.line(df_ts, x="timestamp_prompt", y="count", color=col_name)
    fig.update_layout(height=300, margin={"l": 20, "r": 20, "t": 40, "b": 20})
    return dcc.Graph(figure=fig)


# Initialize Dash App
external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]
app = DjangoDash(
    "DashboardPatientView", external_stylesheets=external_stylesheets
)

# Layout Definition
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
    df_complete = async_to_sync(prepare_user_data)()
    df_complete = process_emotions(df_complete)

    # Date range filtering
    if period != "max":
        months = int(period[:-1])
        start_date = now() - relativedelta(months=months)
        df_complete = filter_data_by_date(df_complete, start_date=start_date)

    mental_bar = create_bar_chart(df_complete, "Mental", n_top)
    psych_bar = create_bar_chart(df_complete, "Psychological", n_top)
    emotion_bar = create_bar_chart(df_complete, "Emotional", n_top)

    # For time series
    mental_ts = create_timeseries_chart(df_complete, "Mental", n_top)
    psych_ts = create_timeseries_chart(df_complete, "Psychological", n_top)
    emotion_ts = create_timeseries_chart(df_complete, "Emotional", n_top)

    n_records = len(df_complete)

    return (
        mental_bar,
        psych_bar,
        emotion_bar,
        mental_ts,
        psych_ts,
        emotion_ts,
        n_records,
    )
