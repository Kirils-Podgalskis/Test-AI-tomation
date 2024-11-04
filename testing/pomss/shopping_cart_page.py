from selenium.webdriver.common.by import By

class ShoppingCartPage():
    shopping_cart_page_container = (By.CSS_SELECTOR,".checkout-cart-index")

    proceed_to_checkout = (By.XPATH, "//span[contains(text(),'Proceed to Checkout')]")

    def __init__(self, driver):
        self.driver = driver