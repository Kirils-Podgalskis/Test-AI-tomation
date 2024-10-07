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
    # TODO: what format shall I provide POMs?n
poms = ['path/to/pom1.py', 'path/to/pom2.py']
poms_strings = []
# for pom in poms:
    # with open(pom, 'r', encoding='utf-8') as file:
    #     pom_string = file.read()
    #     poms_strings.add(pom_string) 

# TODO: makes this a list for comparing different temperatures
TEMPERATURE = 0
additional_information:str = None

prompt = f"Reconstruct compressed test case in <compressed_test_case>.\n<compressed_test_case>\n{compress_test_casess}\n</compressed_test_case>\nUse reconstructed test case to generate a test script.\nFollow compressed project code guidelines for code generation:\n<compressed_guidelines>\n{compressed_guidelines}\n</compressed_guidelines> \nOutput code only."

if additional_information is not None and additional_information is not '':
    prompt += 'Consider following additional information when generating code:\n<additional_information>\n'
    prompt += additional_information
    prompt += '</additional_information>\n'

if len(poms_strings) is not 0:
    prompt += 'Refer to following page object models during test generation:\n<page_object_models>\n'
    for pom_string in poms_strings:
        prompt += f'{pom_string}\n'
    prompt += '</page_object_models>\n'


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
                    "text": prompt 
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
