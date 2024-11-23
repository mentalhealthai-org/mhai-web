from __future__ import annotations

import os

from openai import OpenAI

# Set up your OpenAI API key
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY", ""))
MAX_TOKENS = 256
