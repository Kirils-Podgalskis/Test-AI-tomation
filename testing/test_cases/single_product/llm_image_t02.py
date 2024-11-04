import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from testing.pomss.landing_page import LandingPage
from testing.pomss.shop_header import ShopHeader
from testing.pomss.products_page import ProductsPage
from testing.pomss.single_product_page import SingleProductPage

import pytest

KIRILS_SHOP_URL = 'https://magento.softwaretestingboard.com/'  # Replace with actual URL

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

def test_ajax_sweatshirt_image_navigation(driver):
    """
    Test navigation to Ajax Full-Zip Sweatshirt and image carousel functionality
    """
    landing_page = LandingPage(driver)
    shop_header = ShopHeader(driver)
    products_page = ProductsPage(driver)
    single_product_page = SingleProductPage(driver)

    driver.get('https://magento.softwaretestingboard.com/ajax-full-zip-sweatshirt.html')
    # WebDriverWait(driver, 20).until(
    #     EC.presence_of_element_located(landing_page.landing_container)
    # )

    # men_category = WebDriverWait(driver, 20).until(
    #     EC.element_to_be_clickable(shop_header.men_category)
    # )
    # men_category.click()

    # hoodies_sweatshirts = WebDriverWait(driver, 20).until(
    #     EC.element_to_be_clickable(
    #         products_page.hoodies_and_sweatshirts_buttons
    #     )
    # )
    # hoodies_sweatshirts.click()

    # WebDriverWait(driver, 20).until(
    #     EC.presence_of_element_located(products_page.products_page_container)
    # )

    # ajax_sweatshirt = WebDriverWait(driver, 20).until(
    #     EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, 'Ajax Full-Zip Sweatshirt'))
    # )
    # ajax_sweatshirt.click()

    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located(single_product_page.single_product_page_container)
    )

    product_title = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located(single_product_page.product_page_title)
    )
    assert 'Ajax Full-Zip Sweatshirt' in product_title.text

    first_image = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located(single_product_page.current_image)
    )
    first_image_src = first_image.get_attribute('src')

    right_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable(single_product_page.right_button)
    )
    right_button.click()

    WebDriverWait(driver, 20).until(
        EC.staleness_of(first_image)
    )

    new_image = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located(single_product_page.current_image)
    )
    new_image_src = new_image.get_attribute('src')

    assert first_image_src != new_image_src, 'Image did not change after clicking right button'