from __future__ import annotations

from typing import Any

from mhailib.messages.config import MAX_TOKENS, client


def answer(
    prompt: str, conversation_history: list[dict, Any]
) -> tuple[str, list[dict[str, Any]]]:
    """
    Get a response from the GPT for a given prompt.

    Maintaining the conversation history.

    Parameters
    ----------
    prompt : str
        The user's input prompt.
    conversation_history : list
        The list of message dictionaries maintaining the conversation history.

    Returns
    -------
    str
        The response from the GPT-3 model.
    list[dict[str, Any]]
        conversation_history
    """
    messages = [{"role": "user", "content": prompt}]

    chat_completion = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0.9,
        max_tokens=MAX_TOKENS,
        messages=conversation_history + messages,
    )

    assistant_message = chat_completion.choices[0].message.content

    conversation_history += messages
    conversation_history.append(
        {"role": "assistant", "content": assistant_message}
    )

    return assistant_message, conversation_history
