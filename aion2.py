import requests
import json

API_KEY = "Paste Your API Key Here"

# First API call with reasoning
response = requests.post(
  url="https://openrouter.ai/api/v1/chat/completions",
  headers={
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
  },
  data=json.dumps({
    "model": "aion-labs/aion-2.0",  # Changed to 2.0 (might be cheaper)
    "messages": [
        {
          "role": "user",
          "content": "How many r's are in the word 'strawberry'?"
        }
      ],
    "reasoning": {"enabled": True},
    "max_tokens": 500  # Added to limit token usage
  })
)

# Check if first request succeeded
if response.status_code != 200:
    print(f"First call failed: {response.status_code}")
    print(f"Error: {response.text}")
    exit()

# Extract the assistant message with reasoning_details
response_data = response.json()

# Check for errors in response
if 'error' in response_data:
    print(f"API Error: {response_data['error']}")
    exit()

# Safely extract message
if 'choices' not in response_data or len(response_data['choices']) == 0:
    print(f"Unexpected response format: {response_data}")
    exit()

assistant_msg = response_data['choices'][0]['message']

print("First response:")
print(f"Content: {assistant_msg.get('content')}")
print(f"Reasoning details: {assistant_msg.get('reasoning_details')}")
print("-" * 50)

# Preserve the assistant message with reasoning_details
messages = [
  {"role": "user", "content": "How many r's are in the word 'strawberry'?"},
  {
    "role": "assistant",
    "content": assistant_msg.get('content'),
    "reasoning_details": assistant_msg.get('reasoning_details')  # Pass back unmodified
  },
  {"role": "user", "content": "Are you sure? Think carefully."}
]

# Second API call - model continues reasoning from where it left off
response2 = requests.post(
  url="https://openrouter.ai/api/v1/chat/completions",
  headers={
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
  },
  data=json.dumps({
    "model": "aion-labs/aion-2.0",
    "messages": messages,  # Includes preserved reasoning_details
    "reasoning": {"enabled": True},
    "max_tokens": 500  # Added limit
  })
)

# Check if second request succeeded
if response2.status_code != 200:
    print(f"Second call failed: {response2.status_code}")
    print(f"Error: {response2.text}")
    exit()

response2_data = response2.json()

if 'error' in response2_data:
    print(f"API Error in second call: {response2_data['error']}")
    exit()

if 'choices' in response2_data and len(response2_data['choices']) > 0:
    final_msg = response2_data['choices'][0]['message']
    print("Final response:")
    print(f"Content: {final_msg.get('content')}")
    print(f"Reasoning details: {final_msg.get('reasoning_details')}")
else:
    print(f"Unexpected second response: {response2_data}")