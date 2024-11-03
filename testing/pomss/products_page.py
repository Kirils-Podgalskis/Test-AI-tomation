from selenium.webdriver.common.by import By

class ProductsPage():
    products_page_container = (By.CSS_SELECTOR,'.page-products')

    left_side_bar = (By.CSS_SELECTOR, '.sidebar-main')
    hoodies_and_sweatshirts_buttons = (By.XPATH, "//*[contains(text(),'Hoodies & Sweatshirts')]")

    add_to_cart_buttons = (By.XPATH, "//*[contains(text(),'Add to Cart') and not(ancestor-or-self::script)]")

    price_dropdown = (By.XPATH,"//div[contains(text(),'Price')]")
    range_40__49_99 = (By.CSS_SELECTOR,"a[href*='40-50']")

    all_products = (By.CSS_SELECTOR, ".product-item")
    all_product_prices = (By.CSS_SELECTOR, ".product-items .price")
    all_add_to_cart_buttons = (By.CSS_SELECTOR, ".actions-primary")
    all_add_to_compare_buttons = (By.CSS_SELECTOR, ".tocompare")

    sort_by_select = (By.XPATH,"(//select[@id='sorter'])[1]")
    sort_direction_arrow = (By.XPATH, "(//a[@data-role='direction-switcher'])[1]")

    show_n_item_per_page_select = (By.XPATH, "(//select[@id='limiter'])[2]")


    def __init__(self, driver):
        self.driver = driver
