from selenium.webdriver.common.by import By

class LoginPage():
    login_page_container = (By.CSS_SELECTOR, 'body[class*=customer-account-login]')
    
    email_input = (By.CSS_SELECTOR, '#email')
    email_input_error = (By.CSS_SELECTOR, '#email-error')
    password_input = (By.CSS_SELECTOR, '#pass')
    password_input_error = (By.CSS_SELECTOR, '#pass-error')
    sign_in_button = (By.CSS_SELECTOR, '.columns #send2')
    
    def __init__(self, driver):
        self.driver = driver
