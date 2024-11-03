import os
from anthropic import Anthropic
from dotenv import load_dotenv
from compress_guidelines import compress_guidelines
from compress_test_cases import compress_test_cases
from compress_system_info import compress_system_info
import re
load_dotenv()


API_KEY                     =os.getenv('ANTHROPIC_API_KEY')
COMPRESSED_GUIDELINES_PATH  =os.getenv('COMPRESSED_GUIDELINES_PATH')
COMPRESSED_TEST_CASES       =os.getenv('COMPRESSED_TEST_CASES')
COMPRESSED_SYS_INFO_PATH    =os.getenv('COMPRESSED_SYS_INFO_PATH')
PATH_TO_WRITE_OUTPUT        =os.getenv('PATH_TO_WRITE_OUTPUT')

TEMPERATURE = float(input("Enter temperature:"))

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
    compressed_test_cases = file.read()

# Prepare system info
if not os.path.exists(COMPRESSED_SYS_INFO_PATH):
    compress_system_info()

with open(COMPRESSED_SYS_INFO_PATH, 'r', encoding='utf-8') as file:
    compressed_system_info = file.read()


# Providing POMS
pom_files = set()
while True:
    paths = input("Enter one or multiple file paths (separated by commas) or press Enter to finish: ")
    if paths == "":
        break
    
    pom_files.add(paths)

print("Collected file paths:", pom_files)

# convert files to strings
stringified_poms = []
for pom in pom_files:
    with open(pom, 'r', encoding='utf-8') as file:
        pom_file = file.read()
        selectors = re.findall("\s{4}([A-Za-z_]+)\s*=\s*\(By",pom_file)
        page_name = re.findall("class (\w+)", pom_file)
        stringified_poms.append({page_name[0]:selectors}) 

# add files to query
page_objects:str = ""
if len(stringified_poms) > 0:
    page_objects += 'Refer to following page object models during test generation:\n<page_object_models>\n'
    for pom_string in stringified_poms:
        page_objects += f'{pom_string}\n'
    page_objects += '</page_object_models>\n'

user_provided_information = input("Enter additional information or press Enter to finish: ")
additional_information:str = ""
if user_provided_information is not None and user_provided_information != '':
    additional_information += 'Consider following additional information when generating code:\n<additional_information>\n'
    additional_information += f'{user_provided_information}\n'
    additional_information += '</additional_information>\n'

prompt = f"Reconstruct system descryption in <compressed_system_description> and use this information in future tasks.\n<compressed_system_description>\n{compressed_system_info}\n</compressed_system_description>\nReconstruct compressed test case in <compressed_test_case>.\n<compressed_test_case>\n{compressed_test_cases}\n</compressed_test_case>\nUse reconstructed test case to generate a test script. Generate test script code step-by-step: each action and check must be pepresented by code. Consider, that test case is meant for manual testing, therefore test case may not explicitly mention element waits. Carefully analyze each step and 2 neighboring steps to generate robust test and exlude posibilty of the test producing false negatives during execution.\nFollow compressed project code guidelines for code generation:\n<compressed_guidelines>\n{compressed_guidelines}\n</compressed_guidelines>\n{page_objects}{additional_information}\nOutput code only."

message = client.messages.create(
    model="claude-3-5-sonnet-20240620",
    max_tokens=8192,
    temperature=TEMPERATURE,
    system="You will be using Python 3.10, pytest v8.3.3, and selenium v4.25.0 to generate automated end-to-end test scripts for graphical user interaface test automation.",
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
