from selenium.webdriver.common.by import By

class LandingPage():
    landing_container = (By.CSS_SELECTOR, 'body[class*="cms-home"]')
    

    all_products_previews = (By.CSS_SELECTOR, '.product-item')
    all_products_name = (By.CSS_SELECTOR, '.product-item-name')
    all_products_add_to_card_buttons = (By.CSS_SELECTOR, '.product-item .actions-primary')

    fusion_backpack_preview = (By.CSS_SELECTOR, '.product-item:nth-child(5)')
    
    def __init__(self, driver):
        self.driver = driver
# SIGN_IN = (By.XPATH, "//*[@class='page-header']//*[contains(text(),'Sign In')]")
# CART_CONTAINER = (By.CSS_SELECTOR, '.showcart')
# SEARCH_BAR = (By.CSS_SELECTOR, '#search')

# MEN_CATEGORY = (By.CSS_SELECTOR, "#ui-id-2>.nav-3")
# MEN_CATEGORY_TOOL = (By.CSS_SELECTOR, ".nav-3-1")
# MEN_CATEGORY_TOOL_TANKS = (By.CSS_SELECTOR, ".nav-3-1-4")

# ALL_TOP_CATEGORIES = (By.CSS_SELECTOR, '.level1 > a[href*="tops"]') 
# ALL_HOODIES_AND_SWEATSHIRTS = (By.XPATH, "//*[contains(text(),'Hoodies & Sweatshirts')]")
# ALL_TANKS = (By.CSS_SELECTOR, '.level2 > a[href*="tanks"]')
