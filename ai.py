"""
Thin wrapper around the OpenAI API for text generation.
"""

import os
from openai import AsyncOpenAI

OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
MAX_TOKENS = int(os.getenv("MAX_TOKENS", "500"))

_client: AsyncOpenAI | None = None


def get_client() -> AsyncOpenAI:
    global _client
    if _client is None:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError("OPENAI_API_KEY environment variable is not set.")
        _client = AsyncOpenAI(api_key=api_key)
    return _client


async def generate_text(prompt: str) -> str:
    """Send a prompt to OpenAI and return the generated text."""
    client = get_client()
    response = await client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a professional copywriter and content-writing assistant "
                    "embedded in a Telegram bot. Follow the user's instruction precisely "
                    "and return only the requested content — no extra commentary, no "
                    "markdown headers, no preamble like 'Here is...'."
                ),
            },
            {"role": "user", "content": prompt},
        ],
        max_tokens=MAX_TOKENS,
        temperature=0.85,
    )
    return response.choices[0].message.content.strip()
