Test case N1 Login page Sanity
1. Open main page
2. Click "Sign in" in header
3. See Email input
4. See Password input
5. See Sign In button below Password

Test case N2 Login page Negative
1. Open main page
2. Click "Sign in" in header
3. See "Sign in" on Login page
4. Click "Sign in"
5. See "This is a required field" error under Email and Password

Test case N3 Login page Negative
1. Open main page
2. Click "Sign in" in header
3. Enter "kirils.podgalskis@edu.rtu.lv" in Email
4. Enter "incorrect" in Password
5. Click "Sign in" on Login page
6. See error: "The account sign-in was incorrect or your account is disabled temporarily. Please wait and try again later."

Test case N4 Login page Positive
1. Open main page
2. Click "Sign in" in header
3. Enter "kirils.podgalskis@edu.rtu.lv" in Email
4. Enter "Password123" in Password
5. Click "Sign in" on Login page
6. See My Account tab

Test case N5 Login page Edge case
1. Open main page
2. Click "Sign in" in header
3. Enter "kirils.podgalskis@edu.rtu.lv" in Email
4. Enter "Password123" in Password
5. Click "Sign in" on Login page
6. See My Account page
7. Clear Cookies
8. Refresh page
9. See login page

Test case N6 Login page Negative
1. Open main page
2. Click "Sign in" in header
3. Enter "kirils.podgalskis" in Email
4. Enter "Password123" in Password
5. Click "Sign in" on Login page
6. See error: "Please enter a valid email address (Ex: johndoe@domain.com)." under Email

Test case N7 Login page Security
1. Open main page
2. Click "Sign in" in header
3. Enter "kirils.podgalskis@edu.rtu.lv" in Email
4. Enter SQL injection in Password
5. Click "Sign in" on Login page
6. See error: "The account sign-in was incorrect or your account is disabled temporarily. Please wait and try again later."