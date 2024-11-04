import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from testing.poms.shop_header import ShopHeader
from testing.poms.landing_page import LandingPage
from testing.poms.products_page import ProductsPage
from testing.poms.single_product_page import SingleProductPage

KIRILS_SHOP_URL = 'https://example.com'  # Replace with actual URL

def test_navigate_to_ajax_sweatshirt_and_verify_images(driver):
    """
    Test navigation to Ajax Full-Zip Sweatshirt and image carousel functionality
    """
    driver.get(KIRILS_SHOP_URL)

    header = ShopHeader(driver)
    products_page = ProductsPage(driver)
    single_product_page = SingleProductPage(driver)

    # Hover over "Men" category and click "Hoodies & Sweatshirts"
    men_category = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable(header.men_category)
    )
    webdriver.ActionChains(driver).move_to_element(men_category).perform()

    hoodies_sweatshirts = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable(header.all_hoodies_and_sweatshirts)
    )
    hoodies_sweatshirts.click()

    # Click on "Ajax Full-Zip Sweatshirt"
    ajax_sweatshirt = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, 'Ajax Full-Zip Sweatshirt'))
    )
    ajax_sweatshirt.click()

    # Verify product page title
    WebDriverWait(driver, 20).until(
        EC.text_to_be_present_in_element(
            single_product_page.product_page_title,
            'Ajax Full-Zip Sweatshirt'
        )
    )

    # Verify first image is visible
    first_image = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located(single_product_page.current_image)
    )
    first_image_src = first_image.get_attribute('src')

    # Click right button to change image
    right_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable(single_product_page.right_button)
    )
    right_button.click()

    # Wait for image to change and verify it's different
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located(single_product_page.current_image)
    )
    second_image = driver.find_element(*single_product_page.current_image)
    second_image_src = second_image.get_attribute('src')

    assert first_image_src != second_image_src, 'Image did not change after clicking right button'