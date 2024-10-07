import os
from anthropic import Anthropic
from dotenv import load_dotenv

def compress_test_cases():
    load_dotenv()
    API_KEY=os.getenv('ANTHROPIC_API_KEY')
    TEST_CASES_PATH=os.getenv('TEST_CASES_PATH')
    COMPRESSED_TEST_CASES=os.getenv('COMPRESSED_TEST_CASES')

    client = Anthropic(
        api_key=API_KEY,
    )
    
    if not os.path.exists(TEST_CASES_PATH):
        raise FileNotFoundError(f"Error: The file {TEST_CASES_PATH} does not exist.")
    else:
        with open(TEST_CASES_PATH, 'r', encoding='utf-8') as file:
            target_text = file.read()

    message = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=5000,
        temperature=0,
        system="You are a Claude 3.5 Sonnet trained by Anthropic to compress text. The compressed text should be able to be decompressed by a different Claude 3.5 Sonnet LLM model into the original text. The compression must be lossless, meaning that a different Claude 3.5 Sonnet LLM model should be able to perfectly reconstruct the original text from the compressed representation, without any additional context or information. The compressed text does not need to be human readable, only decompressible by a different Claude 3.5 Sonnet model.",
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

    with open(COMPRESSED_TEST_CASES, 'w', encoding='utf-8') as file:
        for content_block in message.content:
            print(content_block.text)
            file.write(content_block.text)

if __name__ == "__main__":
    compress_test_cases()