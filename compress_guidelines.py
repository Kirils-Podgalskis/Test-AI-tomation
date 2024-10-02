import os
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

API_KEY=os.getenv('ANTHROPIC_API_KEY')

client = Anthropic(
    api_key=API_KEY,
)

with open('guidelines.md', 'r', encoding='utf-8') as file:
    target_text = file.read()


# Replace placeholders like {{TARGET_TEXT}} with real values,
# because the SDK does not support variables.
message = client.messages.create(
    model="claude-3-5-sonnet-20240620",
    max_tokens=1020,
    temperature=0,
    system="""
    You are a LLM trained to compress text. The compression model should purely minimize the number of characters in the compressed text, 
    while maintaining the semantics of the original text. The resulting compressed text does not need to be decompressed into exactly the original text, 
    but should capture the semantics of the original text. The compressed text should be able to be decompressed 
    into a text that is semantically similar to the original text, but does not need to be identical. Return only compressed text.
    """,
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": f"{target_text}"
                }
            ]
        }
    ]
)

with open('compressed_guidelines.md', 'w', encoding='utf-8') as file:
    # Loop through each content block and write to the file
    for content_block in message.content:
        print(content_block.text)
        file.write(content_block.text)