import os
from openai import OpenAI

api_key = os.getenv("OPENROUTER_API_KEY")

if not api_key:
    raise RuntimeError(
        "OPENROUTER_API_KEY is not set. "
        "Run: export OPENROUTER_API_KEY='YOUR_KEY'"
    )

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
)

completion = client.chat.completions.create(
    model="openrouter/free",
    max_tokens=500,
    messages=[
        {
            "role": "user",
            "content": "Explain quantum computing in one sentence."
        }
    ]
)

print(completion.choices[0].message.content)
