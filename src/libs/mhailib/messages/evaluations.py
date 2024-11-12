"""Evaluate messages."""

from __future__ import annotations

import tiktoken

from transformers import pipeline

encoding_cl100k_base = tiktoken.get_encoding("cl100k_base")

# Initialize sentiment analysis pipeline
sentiment_pipeline = pipeline(
    "sentiment-analysis",
    model="nlptown/bert-base-multilingual-uncased-sentiment",
    top_k=None,
)

# Initialize emotion detection pipeline
# (may need fine-tuning or finding a suitable model)
emotion_pipeline = pipeline(
    "text-classification",
    model="j-hartmann/emotion-english-distilroberta-base",
    top_k=None,
)

mentbert_pipeline = pipeline(
    "text-classification",
    model="reab5555/mentBERT",
    top_k=None,
)

psychbert_pipeline = pipeline(
    "text-classification",
    model="mnaylor/psychbert-finetuned-multiclass",
    top_k=None,
)

MAX_TOKENS = 450


def num_tokens_from_string(string: str) -> int:
    """Returns the number of tokens in a text string."""
    return len(encoding_cl100k_base.encode(string))


def truncate_tokens(string: str, max_num_tokens: int) -> str:
    """Returns the number of tokens in a text string."""
    tokens = encoding_cl100k_base.encode(string)
    return encoding_cl100k_base.decode(tokens[:max_num_tokens])


def eval_sentiment(text: str) -> dict[str, float]:
    """
    Get the level of the sentimental.

    Restriction of 512 tokens.
    """
    if not text:
        return {}

    if num_tokens_from_string(text) > MAX_TOKENS:
        text = truncate_tokens(text, MAX_TOKENS)

    try:
        result_raw = sentiment_pipeline(text)
    except Exception:  # noqa: BLE001
        return {}

    return {
        row["label"].lower().replace(" ", "-"): row["score"]
        for row in result_raw
    }


def eval_emotions(text: str) -> dict[str, float]:
    """
    Return
    ------
    dict[str, float]:
        Example:
            {'neutral': 0.8584240078926086,
            'joy': 0.062253180891275406,
            'disgust': 0.029055433347821236,
            'sadness': 0.019559673964977264,
            'anger': 0.01465342566370964,
            'surprise': 0.010109353810548782,
            'fear': 0.0059448955580592155}
    """
    if not text:
        return {}

    if num_tokens_from_string(text) > MAX_TOKENS:
        text = truncate_tokens(text, MAX_TOKENS)

    try:
        result_raw = emotion_pipeline(text)
    except Exception:  # noqa: BLE001
        return {}
    return {
        row["label"].lower().replace(" ", "-"): row["score"]
        for row in result_raw
    }


def eval_psychbert(text: str) -> dict[str, float]:
    """
    This is a version of
    https://huggingface.co/mnaylor/psychbert-cased
    which was fine-tuned to illustrate performance on a multi-class
    classification problem involving the detection of different
    types of language relating to mental health.

    The classes are as follows:

    0: Negative / unrelated to mental health
    1: Mental illnesses
    2: Anxiety
    3: Depression
    4: Social anxiety
    5: Loneliness
    The dataset for this model was taken from Reddit and Twitter,
    and labels were assigned based on the post appearing in certain
    subreddits or containing certain hashtags. For more information,
    see the PsychBERT paper.

    References
    ----------
    https://huggingface.co/mnaylor/psychbert-finetuned-multiclass
    """
    if not text:
        return {}

    label_map = {
        "LABEL_0": "negative",
        "LABEL_1": "mental illnesses",
        "LABEL_2": "anxiety",
        "LABEL_3": "depression",
        "LABEL_4": "social anxiety",
        "LABEL_5": "loneliness",
    }

    if num_tokens_from_string(text) > MAX_TOKENS:
        text = truncate_tokens(text, MAX_TOKENS)

    try:
        result_raw = psychbert_pipeline(text)
    except Exception:  # noqa: BLE001
        return {}

    return {
        (
            label_map.get(row["label"], row["label"]).lower().replace(" ", "-")
        ): row["score"]
        for row in result_raw
    }


def eval_mentbert(text: str) -> dict[str, float]:
    """
    This model is a finetuned BERT (bert-base-uncased)
    model that predict different mental disorders.

    It is trained on a costume dataset of texts or posts
    (from Reddit) about general experiences of users with mental
    health problems.

    Dataset was cleaned and all direct mentions of the disorder
    names in the texts were removed.

    It includes the following classes:

    - Borderline
    - Anxiety
    - Depression
    - Bipolar
    - OCD
    - ADHD
    - Schizophrenia
    - Asperger
    - PTSD

    References
    ----------
    https://huggingface.co/reab5555/mentBERT
    """
    if not text:
        return {}

    if num_tokens_from_string(text) > MAX_TOKENS:
        text = truncate_tokens(text, MAX_TOKENS)

    try:
        result_raw = mentbert_pipeline(text)
    except Exception:  # noqa: BLE001
        return {}

    return {
        row["label"].lower().replace(" ", "-"): row["score"]
        for row in result_raw
    }
