Test Auto code guide:
1. snake_case for funcs/methods
2. <100 chars/line; wrap:
   - indent 1 tab
   - closing paren/bracket new line
   - break post-op/comma
   - binary ops start new line
3. Import order:
   - std lib
   - 3rd party
   - proj POM
   - proj helpers
4. Blank line btw import groups
5. Imports at file top
6. 1 tab indent
7. Docstring for fixtures/tests
8. Single-quotes; double if single inside
9. f-strings for formatting
10. Test names: <func>_<page>_<type>_test()
    <type>: sanity/pos/neg/bound/edge/sec