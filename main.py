import os
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

API_KEY=os.getenv('ANTHROPIC_API_KEY')

client = Anthropic(
    api_key=API_KEY,
)

message = client.messages.create(
    max_tokens=1024,
    messages=[
        {
            "role": "user",
            "content": "Hello, Claude! I am looking forward to work with you and do a reseach on LLM usage for GUI test automation test script generation :)",
        }
    ],
    model="claude-3-5-sonnet-20240620",
)
print(message.content)