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
        system="You are a Claude 3.5 Sonnet trained by Anthropic trained to compress text. The compression model should purely minimize the number of characters in the compressed text, while maintaining the semantics of the original text. The resulting compressed text does not need to be decompressed into exactly the original text, but should capture the semantics of the original text. The compressed text should be able to be decompressed into a text that is semantically similar to the original text, but does not need to be identical. Do not merge nor combine test cases, but preserve test case description, like test number, page under test and type of the test. Preserve string literals in quotes",
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