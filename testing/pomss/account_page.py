from selenium.webdriver.common.by import By

class AccountPage():
    MY_ACCOUNT_PAGE = (By.CSS_SELECTOR,'body[class*="account"]')

    def __init__(self, driver):
        self.driver = driver