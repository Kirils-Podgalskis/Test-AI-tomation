from selenium.webdriver.common.by import By

class ShoppingCartPage():
    SHOPPING_CART_PAGE_CONTAINER = (By.CSS_SELECTOR,".checkout-cart-index")

    PROCEED_TO_CHECKOUT = (By.XPATH, "//span[contains(text(),'Proceed to Checkout')]")