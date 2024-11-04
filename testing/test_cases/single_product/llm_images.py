import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from testing.pomss.shop_header import ShopHeader
from testing.pomss.landing_page import LandingPage
from testing.pomss.products_page import ProductsPage
from testing.pomss.single_product_page import SingleProductPage

import pytest

KIRILS_SHOP_URL = 'https://magento.softwaretestingboard.com/'  # Replace with actual URL
TIMEOUT = 20

@pytest.fixture(scope='function')
def driver():
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service
    chrome_driver_path = '/Users/kirilspodgalskis/Desktop/Test-AI-tomation/testing/tests/chromedriver'
    service = Service(executable_path=chrome_driver_path)
    driver = webdriver.Chrome(service=service)
    driver.maximize_window()
    yield driver

    driver.quit()

def test_navigate_to_ajax_sweatshirt_and_verify_images(driver):
    """
    Test navigation to Ajax Full-Zip Sweatshirt and image carousel functionality
    """
    driver.get('https://magento.softwaretestingboard.com/men/tops-men/hoodies-and-sweatshirts-men.html') ##

    header = ShopHeader(driver)
    products_page = ProductsPage(driver)
    single_product_page = SingleProductPage(driver)

    # # Hover over "Men" category and click "Hoodies & Sweatshirts"
    # men_category = WebDriverWait(driver, 20).until(
    #     EC.element_to_be_clickable(header.men_category)
    # )
    # webdriver.ActionChains(driver).move_to_element(men_category).perform()

    # hoodies_sweatshirts = WebDriverWait(driver, 20).until(
    #     EC.element_to_be_clickable(header.all_hoodies_and_sweatshirts)
    # )
    # hoodies_sweatshirts.click()

    # Click on "Ajax Full-Zip Sweatshirt"

    ajax_sweatshirt = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, 'Ajax Full-Zip Sweatshirt'))
    )
    ajax_sweatshirt.click()

    # Verify product page title
    WebDriverWait(driver, 20).until(
        EC.text_to_be_present_in_element(
            single_product_page.product_page_title, 'Ajax Full-Zip Sweatshirt'
        )
    )

    # Verify first image is visible
    WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located(single_product_page.current_image)
    )
    initial_image_src = driver.find_element(*single_product_page.current_image).get_attribute('src')

        # Click right button and wait for animation
    right_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable(single_product_page.right_button)
    )
    right_button.click()
    time.sleep(3)

    # Verify different image is displayed
    WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located(single_product_page.current_image)
    )
    new_image_src = driver.find_element(*single_product_page.current_image).get_attribute('src')

    assert initial_image_src != new_image_src, 'Image did not change after clicking right button'