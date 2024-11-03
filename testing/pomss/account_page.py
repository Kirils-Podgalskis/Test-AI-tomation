from selenium.webdriver.common.by import By

class AccountPage():
    my_account_page = (By.CSS_SELECTOR,'body[class*="account"]')

    def __init__(self, driver):
        self.driver = driver