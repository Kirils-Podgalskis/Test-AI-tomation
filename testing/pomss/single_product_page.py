from selenium.webdriver.common.by import By

class SingleProductPage():
    SINGLE_PRODUCT_PAGE_CONTAINER = (By.CSS_SELECTOR,'.page-product-configurable')

    PRODUCT_PAGE_TITLE = (By.CSS_SELECTOR, 'span[class="base"]')

    SIZES_CONTAINER = (By.CSS_SELECTOR,"div[class='swatch-attribute size']")
    XS_SIZE_BUTTON = (By.CSS_SELECTOR,'div[option-label="XS"]')

    COLORS_CONTAINER = (By.CSS_SELECTOR, "div[class='swatch-attribute color']")
    BLUE_COLOR_BUTTON = (By.CSS_SELECTOR,'div[option-label="Blue"]')
    RED_COLOR_BUTTON = (By.CSS_SELECTOR,'div[option-label="Red"]')

    QUANITY_INPUT = (By.CSS_SELECTOR,'#qty' )
    
    ALL_ERROR_LABELS = (By.CSS_SELECTOR, "div[class*='mage-error']")

    IMAGE_CONTAINER = (By.CSS_SELECTOR, ".fotorama__grab")
    CURRENT_IMAGE = (By.CSS_SELECTOR,'.fotorama__grab > div[data-active="true"] .fotorama__img')
    RIGHT_BUTTON = (By.CSS_SELECTOR, ".fotorama__arr fotorama__arr--next")

    ADD_TO_CART_BUTTON = (By.CSS_SELECTOR,".actions .primary")

    def __init__(self, driver):
        self.driver = driver
