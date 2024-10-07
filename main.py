import os
from anthropic import Anthropic
from dotenv import load_dotenv
from compress_guidelines import compress_guidelines
from compress_test_cases import compress_test_cases
load_dotenv()

API_KEY                     =os.getenv('ANTHROPIC_API_KEY')
COMPRESSED_GUIDELINES_PATH  =os.getenv('COMPRESSED_GUIDELINES_PATH')
COMPRESSED_TEST_CASES       =os.getenv('COMPRESSED_TEST_CASES')
PATH_TO_WRITE_OUTPUT        =os.getenv('PATH_TO_WRITE_OUTPUT')

# TODO: makes this a list for comparing different temperatures
TEMPERATURE = 0

client = Anthropic(
    api_key=API_KEY,
)

# Prepare guidelines
if not os.path.exists(COMPRESSED_GUIDELINES_PATH):
    compress_guidelines()

with open(COMPRESSED_GUIDELINES_PATH, 'r', encoding='utf-8') as file:
    compressed_guidelines = file.read()

# Prepare test case
if not os.path.exists(COMPRESSED_TEST_CASES):
    compress_test_cases()

with open(COMPRESSED_TEST_CASES, 'r', encoding='utf-8') as file:
    compress_test_casess = file.read()

# TODO: provide POMs
    # TODO: what format shall I provide POMs?
# TODO: prompt user for additional information
# TODO: provide modal currently available test cases with pytest --cleat-test,
#   so it pottentially skip certain test generation?

message = client.messages.create(
    model="claude-3-5-sonnet-20240620",
    max_tokens=5000,
    temperature=TEMPERATURE,
    system="You will be using Python 3.10, pytest v8.3.3, and selenium v4.25.0 to generate automated end-to-end test scripts.",
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": f"Reconstruct compressed test case in <compressed_test_case>.\n<compressed_test_case>\n{compress_test_casess}\n</compressed_test_case>\nUse reconstructed test case to generate a test script.\nFollow compressed project code guidelines for code generation:\n<compressed_guidelines>\n{compressed_guidelines}\n</compressed_guidelines> \nOutput code only."
                    # TODO: make  
                }
            ]
        }
    ]
)

for content_block in message.content:
    print(content_block.text)

with open(PATH_TO_WRITE_OUTPUT, 'a', encoding='utf-8') as file:
    for content_block in message.content:
        file.write(content_block.text)
