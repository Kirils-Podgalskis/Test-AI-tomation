import time
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

from testing.pomss.shop_header import ShopHeader
from testing.pomss.products_page import ProductsPage


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


def test_price_filter_boundary_products_page(driver):
    """
    Test price filter boundary for men's hoodies & sweatshirts.
    """
    driver.get(KIRILS_SHOP_URL)
    
    header = ShopHeader(driver)
    products_page = ProductsPage(driver)
    
    # Hover over "Men" category to reveal dropdown
    men_category = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located(header.men_category)
    )
    ActionChains(driver).move_to_element(men_category).perform()
    
    # Click on "Hoodies & Sweatshirts" in the dropdown
    hoodies_sweatshirts = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable(header.all_hoodies_and_sweatshirts)
    )
    hoodies_sweatshirts.click()
    
    # Wait for the products page to load
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located(products_page.products_page_container)
    )
    
    # Click on the price dropdown
    price_dropdown = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable(products_page.price_dropdown)
    )
    price_dropdown.click()
    
    # Select the $40-49.99 range
    price_range = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable(products_page.range_40__49_99)
    )
    price_range.click()
    
    # Wait for the page to update with filtered results
    time.sleep(2)  # Allow time for AJAX update
    
    # Get all product prices
    product_prices = WebDriverWait(driver, 20).until(
        EC.presence_of_all_elements_located(products_page.all_product_prices)
    )
    
    # Check that no price is less than $40 or greater than $49.99
    for price_element in product_prices:
        price_text = price_element.text.strip('$')
        price = float(price_text)
        
        assert 40 <= price <= 49.99, (
            f'Price ${price} is outside the expected range of $40-$49.99'
        )