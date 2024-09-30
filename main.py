import os
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

API_KEY=os.getenv('ANTHROPIC_API_KEY')

client = Anthropic(
    api_key=API_KEY,
)

# TODO: compress test case, flag test_case_compresse = true
# TODO: compress guidline, guidelines_compressed = true
# prompt user for additional information

message = client.messages.create(
    max_tokens=1024,
    messages=[
        {
            "role": "user",
            "content": "What's my name?",
        }
    ],
    model="claude-3-5-sonnet-20240620",
    temperature=0.4
)
for content_block in message.content:
    print(content_block.text)
