import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from testing.pomss.landing_page import LandingPage
from testing.pomss.shop_header import ShopHeader
from testing.pomss.products_page import ProductsPage

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

def test_main_page_sanity_sign_in(driver):
    """Test presence of Sign In button on main page."""
    driver.get(KIRILS_SHOP_URL)
    
    header = ShopHeader(driver)
    WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located(header.sign_in)
    )

    assert header.sign_in.is_displayed() ## 

def test_main_page_sanity_cart(driver):
    """Test presence of Cart button on main page."""
    driver.get(KIRILS_SHOP_URL)
    
    header = ShopHeader(driver)
    WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located(header.cart_container)
    )

    assert header.cart_container.is_displayed() ##

def test_main_page_sanity_products(driver):
    """Test presence of specific products on main page."""
    driver.get(KIRILS_SHOP_URL)
    
    landing = LandingPage(driver)
    WebDriverWait(driver, 20).until(
        EC.presence_of_all_elements_located(landing.all_products_name)
    )
    
    driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
    time.sleep(1)  # Allow time for any lazy-loaded elements

    product_names = [p.text for p in landing.all_products_name] ##
    expected_products = [
        'Radiant Tee', 'Breathe-Easy Tank', 'Argus All-Weather Tank',
        'Hero Hoodie', 'Fusion Backpack', 'Push It Messenger Bag'
    ]

    assert all(product in product_names for product in expected_products)

def test_main_page_sanity_add_to_cart_hover(driver):
    """Test 'Add to Cart' button appears on product hover."""
    driver.get(KIRILS_SHOP_URL)
    
    landing = LandingPage(driver)
    WebDriverWait(driver, 20).until(
        EC.presence_of_all_elements_located(landing.all_products_previews)
    )
    
    driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
    time.sleep(1)  # Allow time for any lazy-loaded elements

    first_product = landing.all_products_previews[0] ##
    driver.execute_script('arguments[0].scrollIntoView();', first_product) ##
    
    actions = webdriver.ActionChains(driver) ## 
    actions.move_to_element(first_product).perform()
    
    WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located(landing.all_products_add_to_card_buttons[0]) ##
    )

    assert landing.all_products_add_to_card_buttons[0].is_displayed() ##

def test_main_page_positive_add_to_cart_no_hover(driver):
    """Test 'Add to Cart' button is not visible without hover."""
    driver.get(KIRILS_SHOP_URL)
    
    landing = LandingPage(driver)
    WebDriverWait(driver, 20).until(
        EC.presence_of_all_elements_located(landing.all_products_previews)
    )
    
    driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
    time.sleep(1)  # Allow time for any lazy-loaded elements

    assert not landing.all_products_add_to_card_buttons[0].is_displayed() ##

def test_main_page_positive_search(driver):
    """Test search functionality with valid input."""
    driver.get(KIRILS_SHOP_URL)
    
    header = ShopHeader(driver)
    WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located(header.search_bar)
    )
    
    header.search_bar.send_keys('T shirt') ##
    header.search_bar.send_keys(Keys.RETURN) ##
    
    products = ProductsPage(driver)
    WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located(products.products_page_container)
    )
    
    assert len(products.all_products) >= 1 ##

def test_main_page_negative_empty_search(driver):
    """Test empty search keeps user on main page."""
    driver.get(KIRILS_SHOP_URL)
    
    header = ShopHeader(driver)
    WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located(header.search_bar)
    )
    
    header.search_bar.click() ## 
    header.search_bar.send_keys(Keys.RETURN) ##
    
    landing = LandingPage(driver)
    
    assert WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located(landing.landing_container)
    )

def test_main_page_boundary_search_input(driver):
    """Test search input character limit."""
    driver.get(KIRILS_SHOP_URL)
    
    header = ShopHeader(driver)
    WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located(header.search_bar)
    )
    
    long_input = 'a' * 130
    header.search_bar.send_keys(long_input) ## 
    
    actual_input = header.search_bar.get_attribute('value') ##
    
    assert len(actual_input) == 128

def test_main_page_positive_category_navigation(driver):
    """Test category navigation from main page."""
    driver.get(KIRILS_SHOP_URL)
    
    header = ShopHeader(driver)
    WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located(header.men_category)
    )
    
    actions = webdriver.ActionChains(driver) ##
    actions.move_to_element(header.men_category).perform()
    WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located(header.men_category_tool)
    )
    
    actions.move_to_element(header.men_category_tool).perform() 
    WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located(header.men_category_tool_tanks)
    )
    
    header.men_category_tool_tanks.click() ##
    
    products = ProductsPage(driver)
    WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located(products.products_page_container)
    )
    
    assert 'Tanks' in driver.title ##
    assert len(products.all_products) == 12 ##