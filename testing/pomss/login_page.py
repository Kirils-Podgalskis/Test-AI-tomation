from selenium.webdriver.common.by import By

class LoginPage():
    LOGIN_PAGE_CONTAINER = (By.CSS_SELECTOR, 'body[class*=customer-account-login]')
    
    EMAIL_INPUT = (By.CSS_SELECTOR, '#email')
    EMAIL_INPUT_ERROR = (By.CSS_SELECTOR, '#email-error')
    PASSWORD_INPUT = (By.CSS_SELECTOR, '#pass')
    PASSWORD_INPUT_ERROR = (By.CSS_SELECTOR, '#pass-error')

    def __init__(self, driver):
        self.driver = driver
