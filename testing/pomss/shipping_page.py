from selenium.webdriver.common.by import By

class ShippingPage():
    SHIPPING_PAGE_CONTAINER = (By.CSS_SELECTOR,".checkout-index-index")

    EMAIL_INPUT = (By.CSS_SELECTOR, "#shipping #customer-email")
    PASSWORD_INPUT = (By.CSS_SELECTOR, "#shipping #customer-password")
    FIRST_NAME_INPUT = (By.CSS_SELECTOR, "#shipping input[name='firstname']")
    STREET_INPUT = (By.CSS_SELECTOR, "#shipping input[name='street[0]']")
    CITY_INPUT = (By.CSS_SELECTOR, "#shipping input[name='city']")
    ZIP_PASTCODE_INPUT = (By.CSS_SELECTOR, "#shipping input[name='postcode']")
    STATE_PROVICE_SELECT = (By.CSS_SELECTOR,"#shipping select[name='region_id']")
    COUNTRY_SELECT = (By.CSS_SELECTOR, "#shipping select[name='country_id']")
    PHONE_NUMBER = (By.CSS_SELECTOR, "#shipping input[name='telephone']")

    NEXT_BUTTON = (By.CSS_SELECTOR, ".continue")
    PLACE_ORDER_BUTTON = (By.CSS_SELECTOR,'.primary .checkout')
    
    ORDER_NUMBER_LABEL =(By.CSS_SELECTOR,".checkout-success > p:nth-child(1)")
    
    def __init__(self, driver):
        self.driver = driver