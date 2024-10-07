Test case T1 boundary test:
- Open "search product" page
- Search for products with price less than 1.00
- Wait for products to load
- Assert error "Minimum search price is 1.00" is displayed
- Assert that price filter is set to 1.00

Test case T2 sanity:
- Open "login" page
- enter known test credentials
- click login button
- assert main page of the app is displayed

Test case T3 security test:
- Open "login" page
- enter username
- enter SQL injection as password
- click login
- assert error message is displayed

Test case T4 boundary test:
- Open "search product" page
- Search for products with price 999999
- Wait for products to load
- Assert error "Maximum search price is 100'000" is displayed
- Assert that price filter is set to 100'000

Test case T5 boundary test:
- Open "search product" page
- Search for products with price 100000
- Wait for products to load
- Assert no product on the page has price more than 100000 

Test case T6 edge case test:
- Open "register" page
- Enter new username "username<current_timestamp()>"
- Enter password "password123"
- Enter email "non_existing_email@kirilspodgalskis.com"
- Click register button
- Assert error "Invalid email is provided" is displayed

