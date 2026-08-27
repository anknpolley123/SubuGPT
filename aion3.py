import requests
import json

API_KEY = "Paste your API key here"

response = requests.post(
  url="https://openrouter.ai/api/v1/chat/completions",
  headers={
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
  },
  data=json.dumps({
    "model": "aion-labs/aion-3.0",
    "messages": [
        {
          "role": "user",
          "content": "How many r's are in the word 'strawberry'?"
        }
      ],
    "reasoning": {"enabled": True},
    "max_tokens": 500  # Limit output to 500 tokens
  })
)

print(f"Status: {response.status_code}")
if response.status_code == 200:
    data = response.json()
    print(data['choices'][0]['message']['content'])
else:
    print(f"Error: {response.text}")