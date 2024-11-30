#!/usr/bin/env python

# In[1]:


from datetime import datetime, timedelta

import joblib
import numpy as np
import pandas as pd
import plotly.express as px

from dash import Input, Output, callback, dcc, html
from dateutil.relativedelta import relativedelta
from django_plotly_dash import DjangoDash


def random_date(days_ago):
    end = datetime.now()
    start = end - timedelta(days=days_ago)
    return start + (end - start) * np.random.rand()

# Add pathlib to handle the data path in basedir
df = joblib.load("/opt/services/mhai-web/data/result.pkl")


df = df[df["question"].notnull()]


df["date"] = [random_date(365) for _ in range(len(df))]
df.insert(0, "date", df.pop("date"))


categories = [
    {"label": "Mental", "value": "mentbert"},
    {"label": "Psychological", "value": "psychbert"},
    {"label": "Emotional", "value": "emotion"},
]


emotions = [
    "fear",
    "sadness",
    "neutral",
    "joy",
    "surprise",
    "anger",
    "disgust",
]

df["emotion_idx"] = np.argmax(
    [
        df["fear"],
        df["sadness"],
        df["neutral"],
        df["joy"],
        df["surprise"],
        df["anger"],
        df["disgust"],
    ],
    axis=0,
)
df["emotion_label"] = df.apply(lambda x: emotions[x["emotion_idx"]], axis=1)

df_filtered = df.copy()


def get_col_name(label):
    global categories

    col_name = [
        item["value"] + "_label"
        for item in categories
        if item["label"] == label
    ][0]

    return col_name


def get_df_filtered(df, start_date=None, end_date=None):
    if start_date == None:
        start_date = df["date"].min()

    if end_date == None:
        end_date = datetime.today().date()

    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)

    df_filtered = df[(df["date"] >= start_date) & (df["date"] < end_date)]

    return df_filtered


def get_df_freq(df, label, top, start_date=None, end_date=None):
    col_name = get_col_name(label)

    df_freq = (
        df[col_name]
        .value_counts()
        .to_frame()
        .reset_index()
        .rename(columns={col_name: "label"})
    )

    return df_freq[0:top]


def get_df_timeseries(df, label, top, start_date=None, end_date=None):
    col_name = get_col_name(label)

    top_items = get_df_freq(df, label, top, start_date, end_date)[
        "label"
    ].values

    df_ts = df[["date", col_name]].rename(columns={col_name: "label"})
    df_ts = df_ts[df_ts["label"].isin(top_items)]
    df_ts["month_year"] = df_ts["date"].dt.to_period("M").dt.to_timestamp()
    df_ts_grouped = (
        df_ts.groupby(["month_year", "label"]).size().reset_index(name="count")
    )
    df_ts_pivot = df_ts_grouped.pivot(
        index="month_year", columns="label", values="count"
    ).reset_index()
    df_ts_pivot = df_ts_pivot.fillna(0)

    return df_ts_pivot


label_mental = "Mental"
label_psych = "Psychological"
label_emotion = "Emotional"

periods = ["Max", "1 month", "3 months", "6 months", "12 months"]

style_block = {
    "border": "1px solid #ccc",
    "border-radius": "10px",
    "padding": "10px",
    "box-shadow": "2px 2px 8px rgba(0, 0, 0, 0.1)",
    "width": "30%",
    "background-color": "#f9f9f9",
}

style_label = {
    "display": "block",
    "margin-bottom": "10px",
    "font-weight": "bold",
}

style_input = {
    "width": "80px",
    "border": "1px solid #ccc",
    "border-radius": "5px",
    "padding": "10px",
}


external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

app = DjangoDash("SimpleExample4", external_stylesheets=external_stylesheets)


def get_bar_graph(category_label, n_top, period):
    global df_filtered

    if category_label == None:
        return None

    start_date = None

    if period != None and period != "Max":
        months = int(period.split(" ")[0])
        start_date = datetime.today().date() - relativedelta(months=months)

    df_freq = get_df_freq(df_filtered, category_label, n_top, start_date)

    fig = px.bar(data_frame=df_freq, x="label", y="count")
    fig.update_traces(width=0.5)
    fig.update_xaxes(title_text="", tickfont=dict(size=12), tickangle=345)
    fig.update_yaxes(title_text="Frequency")
    fig.update_layout(height=260, margin=dict(l=0, r=0, t=25, b=30))

    return dcc.Graph(id=category_label.lower() + "-graph", figure=fig)


def get_timeseries_graph(category_label, n_top, period):
    global df_filtered

    if category_label == None:
        return None

    start_date = None

    if period != None and period != "Max":
        months = int(period.split(" ")[0])
        start_date = datetime.today().date() - relativedelta(months=months)

    df_ts = get_df_timeseries(df_filtered, category_label, n_top, start_date)

    fig = px.line(df_ts, x="month_year", y=df_ts.columns)
    fig.update_xaxes(title_text="", tickfont=dict(size=12), tickangle=345)
    fig.update_yaxes(title_text="")
    fig.update_layout(height=260, margin=dict(l=0, r=0, t=25, b=30))

    return dcc.Graph(id=category_label.lower() + "-graph-ts", figure=fig)


app.layout = html.Div(
    children=[
        html.Div(
            style={"display": "flex", "justify-content": "space-between"},
            children=[
                html.Div(
                    style=style_block,
                    children=[
                        html.Label("Top Items", style=style_label),
                        dcc.Input(
                            id="txt-n-top",
                            value=3,
                            type="number",
                            min=2,
                            max=10,
                            step=1,
                            style=style_input,
                        ),
                    ],
                ),
                html.Div(
                    style=style_block,
                    children=[
                        html.Label("Period", style=style_label),
                        html.Div(
                            style={"display": "inline-flex"},
                            children=[
                                dcc.Dropdown(
                                    id="drop-period",
                                    options=periods,
                                    value="Max",
                                    style={"width": "200px"},
                                )
                            ],
                        ),
                    ],
                ),
                html.Div(
                    style=style_block,
                    children=[
                        html.Label("Records", style=style_label),
                        dcc.Input(
                            id="txt-records", disabled=True, style=style_input
                        ),
                    ],
                ),
            ],
        ),
        html.Div(
            children=[
                html.H2(
                    label_mental,
                    style={"text-align": "center", "margin": "20px 0 0 0"},
                ),
                html.Div(
                    style={
                        "display": "flex",
                        "justify-content": "space-between",
                    },
                    children=[
                        html.Div(
                            style={"width": "35%"},
                            children=[html.Div(id="div-mental")],
                        ),
                        html.Div(
                            style={"width": "65%"},
                            children=[html.Div(id="div-mental-ts")],
                        ),
                    ],
                ),
            ]
        ),
        html.Div(
            children=[
                html.H2(
                    label_psych,
                    style={"text-align": "center", "margin": "20px 0 0 0"},
                ),
                html.Div(
                    style={
                        "display": "flex",
                        "justify-content": "space-between",
                    },
                    children=[
                        html.Div(
                            style={"width": "35%"},
                            children=[html.Div(id="div-psychological")],
                        ),
                        html.Div(
                            style={"width": "65%"},
                            children=[html.Div(id="div-psychological-ts")],
                        ),
                    ],
                ),
            ]
        ),
        html.Div(
            children=[
                html.H2(
                    label_emotion,
                    style={"text-align": "center", "margin": "20px 0 0 0"},
                ),
                html.Div(
                    style={
                        "display": "flex",
                        "justify-content": "space-between",
                    },
                    children=[
                        html.Div(
                            style={"width": "35%"},
                            children=[html.Div(id="div-emotional")],
                        ),
                        html.Div(
                            style={"width": "65%"},
                            children=[html.Div(id="div-emotional-ts")],
                        ),
                    ],
                ),
            ]
        ),
    ]
)


@callback(
    Output("div-mental", "children"),
    Output("div-psychological", "children"),
    Output("div-emotional", "children"),
    Output("div-mental-ts", "children"),
    Output("div-psychological-ts", "children"),
    Output("div-emotional-ts", "children"),
    Output("txt-records", "value"),
    Input("txt-n-top", "value"),
    Input("drop-period", "value"),
)
def update_graphs(n_top, period):
    global df_filtered

    start_date = None

    if period != None and period != "Max":
        months = int(period.split(" ")[0])
        start_date = datetime.today().date() - relativedelta(months=months)

    df_filtered = get_df_filtered(df, start_date)

    mental_bar = get_bar_graph(label_mental, n_top, period)
    psych_bar = get_bar_graph(label_psych, n_top, period)
    emotion_bar = get_bar_graph(label_emotion, n_top, period)
    mental_ts = get_timeseries_graph(label_mental, n_top, period)
    psych_ts = get_timeseries_graph(label_psych, n_top, period)
    emotion_ts = get_timeseries_graph(label_emotion, n_top, period)
    n_records = len(df_filtered)

    return (
        mental_bar,
        psych_bar,
        emotion_bar,
        mental_ts,
        psych_ts,
        emotion_ts,
        n_records,
    )
