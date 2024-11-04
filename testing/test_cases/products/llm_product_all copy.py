import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

from testing.pomss.landing_page import LandingPage
from testing.pomss.products_page import ProductsPage
from testing.pomss.shop_header import ShopHeader

import pytest

KIRILS_SHOP_URL = 'https://magento.softwaretestingboard.com/'  # Replace with actual URL
TIMEOUT = 20

@pytest.fixture(scope='function')
def driver():
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.chrome.options import Options
    chrome_driver_path = '/Users/kirilspodgalskis/Desktop/Test-AI-tomation/testing/tests/chromedriver'
    service = Service(executable_path=chrome_driver_path)
    options = Options()
    options.add_extension('/Users/kirilspodgalskis/Desktop/Test-AI-tomation/testing/tests/CJPALHDLNBPAFIAMEJDNHCPHJBKEIAGM_1_60_0_0.crx')
    driver = webdriver.Chrome(service=service, options=options)

    yield driver

    driver.quit()
TIMEOUT = 20

@pytest.fixture(scope='function')
def driver():
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.chrome.options import Options
    chrome_driver_path = '/Users/kirilspodgalskis/Desktop/Test-AI-tomation/testing/tests/chromedriver'
    service = Service(executable_path=chrome_driver_path)
    options = Options()
    options.add_extension('/Users/kirilspodgalskis/Desktop/Test-AI-tomation/testing/tests/CJPALHDLNBPAFIAMEJDNHCPHJBKEIAGM_1_60_0_0.crx')
    driver = webdriver.Chrome(service=service, options=options)

    yield driver

    driver.quit()

def test_price_filter_boundary_products_page(driver):
    """
    Test price filter boundary on products page for men's hoodies & sweatshirts.
    """
    driver.get(KIRILS_SHOP_URL)
    
    landing_page = LandingPage(driver)
    products_page = ProductsPage(driver)
    shop_header = ShopHeader(driver)
    
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located(landing_page.landing_container)
    )
    
    men_category = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable(shop_header.men_category)
    )
    men_category.click()
    
    hoodies_sweatshirts = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable(products_page.hoodies_and_sweatshirts_buttons)
    )
    hoodies_sweatshirts.click()
    
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located(products_page.products_page_container)
    )
    
    price_dropdown = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable(products_page.price_dropdown)
    )
    price_dropdown.click()
    
    price_range = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable(products_page.range_40__49_99)
    )
    price_range.click()
    
    time.sleep(2)  # Allow time for products to update
    
    product_prices = WebDriverWait(driver, 20).until(
        EC.presence_of_all_elements_located(products_page.all_product_prices)
    )
    
    prices = [float(price.text.replace('$', '')) for price in product_prices]
    
    assert all(40 <= price <= 49.99 for price in prices), (
        'Some products are outside the $40-$49.99 price range'
    )