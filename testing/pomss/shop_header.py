from selenium.webdriver.common.by import By

class ShopHeader():
    sign_in = (By.XPATH, "//*[@class='page-header']//*[contains(text(),'Sign In')]")
    cart_container = (By.CSS_SELECTOR, '.showcart')
    cart_counter = (By.CSS_SELECTOR, '.counter-number')
    search_bar = (By.CSS_SELECTOR, '#search')

    message_banner = (By.CSS_SELECTOR, 'div[class="page messages"]')

    men_category = (By.CSS_SELECTOR, "#ui-id-2>.nav-3")
    men_category_tool = (By.CSS_SELECTOR, ".nav-3-1")
    men_category_tool_tanks = (By.CSS_SELECTOR, ".nav-3-1-4")

    all_top_categories = (By.CSS_SELECTOR, '.level1 > a[href*="tops"]') 
    all_hoodies_and_sweatshirts = (By.XPATH, "//*[contains(text(),'Hoodies & Sweatshirts')]")
    all_tanks = (By.CSS_SELECTOR, '.level2 > a[href*="tanks"]')

    def __init__(self, driver):
        self.driver = driver