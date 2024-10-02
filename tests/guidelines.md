Test Automation code guidelines
1. all functions and methods are written in snake_case
2. each line length is less than 100 characters. If line is longer than 100 characters, line should be wrapped
    - when wrapping, each line should be indented 1 tab from the previous line
    - when wrapping, the closing parenthesis/bracket should be on a new line
    - break after operator
    - break after comma
    - binary operators should be placed at the beginning of the new line
3. import statements are grouped in the following order:
    - standard library imports
    - related third party imports
    - project page object modal imports
    - project helper functions imports
4. import groups are separated by a blank line
5. all import statements are placed at the top of the file
6. indentation is 1 tab
7. all fixtures and test methods have a python docstring, with test description
8. use single-quotes for string literals. Use double-quotes if string literal contains single-quote
9. use f-strings for string formatting rather than the .format() method
10. use following format for test method names: `<tested_functionality>_<tested_page>_<type>_test()`, where `<type>` is one of the following: `sanity`, `positive`, `negative`, `boundary`, `edge`, `security`