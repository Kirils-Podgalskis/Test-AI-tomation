from selenium.webdriver.common.by import By

class SingleProductPage():
    single_product_page_container = (By.CSS_SELECTOR,'.page-product-configurable')

    product_page_title = (By.CSS_SELECTOR, 'span[class="base"]')

    sizes_container = (By.CSS_SELECTOR,"div[class='swatch-attribute size']")
    xs_size_button = (By.CSS_SELECTOR,'div[option-label="XS"]')

    colors_container = (By.CSS_SELECTOR, "div[class='swatch-attribute color']")
    blue_color_button = (By.CSS_SELECTOR,'div[option-label="Blue"]')
    red_color_button = (By.CSS_SELECTOR,'div[option-label="Red"]')

    quanity_input = (By.CSS_SELECTOR,'#qty' )
    
    all_error_labels = (By.CSS_SELECTOR, "div[class*='mage-error']")

    image_container = (By.CSS_SELECTOR, ".fotorama__grab")
    current_image = (By.CSS_SELECTOR,'.fotorama__grab > div[data-active="true"] .fotorama__img')
    right_button = (By.CSS_SELECTOR, "div[class$='fotorama__wrap--toggle-arrows'] .fotorama__arr--next")

    add_to_cart_button = (By.CSS_SELECTOR,".actions .primary")

    def __init__(self, driver):
        self.driver = driver
