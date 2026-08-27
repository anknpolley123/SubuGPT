from openrouter import OpenRouter
import os


API_KEY = "Paste Your API Key Here"

try:
    with OpenRouter(
        api_key=os.getenv("OPENROUTER_API_KEY", API_KEY),
    ) as client:
        response = client.chat.send(
            model="amazon/nova-lite-v1",  
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "What is in this image?"
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": "https://live.staticflickr.com/3851/14825276609_098cac593d_b.jpg"
                            }
                        }
                    ]
                }
            ],
            max_tokens=500  # Limit token usage
        )
        
        # Print the response
        print("Response:")
        print(response.choices[0].message.content)
        
except Exception as e:
    print(f"Error occurred: {e}")
    if hasattr(e, 'response'):
        print(f"Status code: {e.response.status_code}")
        print(f"Response text: {e.response.text}")