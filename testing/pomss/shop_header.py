from selenium.webdriver.common.by import By

class ShopHeader():
    SIGN_IN = (By.XPATH, "//*[@class='page-header']//*[contains(text(),'Sign In')]")
    CART_CONTAINER = (By.CSS_SELECTOR, '.showcart')
    CART_COUNTER = (By.CSS_SELECTOR, '.counter-number')
    SEARCH_BAR = (By.CSS_SELECTOR, '#search')

    MESSAGE_BANNER = (By.CSS_SELECTOR, 'div[class="page messages"]')

    MEN_CATEGORY = (By.CSS_SELECTOR, "#ui-id-2>.nav-3")
    MEN_CATEGORY_TOOL = (By.CSS_SELECTOR, ".nav-3-1")
    MEN_CATEGORY_TOOL_TANKS = (By.CSS_SELECTOR, ".nav-3-1-4")

    ALL_TOP_CATEGORIES = (By.CSS_SELECTOR, '.level1 > a[href*="tops"]') 
    ALL_HOODIES_AND_SWEATSHIRTS = (By.XPATH, "//*[contains(text(),'Hoodies & Sweatshirts')]")
    ALL_TANKS = (By.CSS_SELECTOR, '.level2 > a[href*="tanks"]')

    def __init__(self, driver):
        self.driver = driver