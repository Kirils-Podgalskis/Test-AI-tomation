from selenium.webdriver.common.by import By

class ShippingPage():
    shipping_page_container = (By.CSS_SELECTOR,".checkout-index-index")

    email_input = (By.CSS_SELECTOR, "#shipping #customer-email")
    password_input = (By.CSS_SELECTOR, "#shipping #customer-password")
    first_name_input = (By.CSS_SELECTOR, "#shipping input[name='firstname']")
    street_input = (By.CSS_SELECTOR, "#shipping input[name='street[0]']")
    city_input = (By.CSS_SELECTOR, "#shipping input[name='city']")
    zip_pastcode_input = (By.CSS_SELECTOR, "#shipping input[name='postcode']")
    state_provice_select = (By.CSS_SELECTOR,"#shipping select[name='region_id']")
    country_select = (By.CSS_SELECTOR, "#shipping select[name='country_id']")
    phone_number = (By.CSS_SELECTOR, "#shipping input[name='telephone']")

    next_button = (By.CSS_SELECTOR, ".continue")
    place_order_button = (By.CSS_SELECTOR,'.primary .checkout')
    
    order_number_label =(By.CSS_SELECTOR,".checkout-success > p:nth-child(1)")
    
    def __init__(self, driver):
        self.driver = driver