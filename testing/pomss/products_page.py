from selenium.webdriver.common.by import By

class ProductsPage():
    PRODUCTS_PAGE_CONTAINER = (By.CSS_SELECTOR,'.page-products')

    LEFT_SIDE_BAR = (By.CSS_SELECTOR, '.sidebar-main')
    HOODIES_AND_SWEATSHIRTS_BUTTONS = (By.XPATH, "//*[contains(text(),'Hoodies & Sweatshirts')]")

    ADD_TO_CART_BUTTONS = (By.XPATH, "//*[contains(text(),'Add to Cart') and not(ancestor-or-self::script)]")

    PRICE_DROPDOWN = (By.XPATH,"//div[contains(text(),'Price')]")
    RANGE_40__49_99 = (By.CSS_SELECTOR,"a[href*='40-50']")

    ALL_PRODUCTS = (By.CSS_SELECTOR, ".product-item")
    ALL_PRODUCT_PRICES = (By.CSS_SELECTOR, ".product-items .price")
    ALL_ADD_TO_CART_BUTTONS = (By.CSS_SELECTOR, ".actions-primary")
    ALL_ADD_TO_COMPARE_BUTTONS = (By.CSS_SELECTOR, ".tocompare")

    SORT_BY_SELECT = (By.XPATH,"(//select[@id='sorter'])[1]")
    SORT_DIRECTION_ARROW = (By.XPATH, "(//a[@data-role='direction-switcher'])[1]")

    SHOW_N_ITEM_PER_PAGE_SELECT = (By.XPATH, "(//select[@id='limiter'])[2]")


    def __init__(self, driver):
        self.driver = driver
