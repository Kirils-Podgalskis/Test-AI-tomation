import pytest
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC

from testing.pomss.landing_page import LandingPage
from testing.pomss.products_page import ProductsPage
from testing.pomss.shop_header import ShopHeader

KIRILS_SHOP_URL = 'https://magento.softwaretestingboard.com/'  # Replace with actual URL

@pytest.fixture
def driver():
    chrome_driver_path = '/Users/kirilspodgalskis/Desktop/Test-AI-tomation/testing/tests/chromedriver'
    service = Service(executable_path=chrome_driver_path)
    options = Options()
    options.add_extension('/Users/kirilspodgalskis/Desktop/Test-AI-tomation/testing/tests/CJPALHDLNBPAFIAMEJDNHCPHJBKEIAGM_1_60_0_0.crx')
    driver = webdriver.Chrome(service=service, options=options)
    driver.maximize_window()

    yield driver

    driver.quit()


def test_main_sanity_sign_in(driver):
    """Test presence of Sign In button on main page"""
    driver.get(KIRILS_SHOP_URL)
    
    wait = WebDriverWait(driver, 20)
    sign_in_btn = wait.until(EC.presence_of_element_located(ShopHeader.SIGN_IN))
    
    assert sign_in_btn.is_displayed()

def test_main_sanity_cart(driver:webdriver):
    """Test presence of Cart button on main page"""
    driver.get(KIRILS_SHOP_URL)
    
    wait = WebDriverWait(driver, 20)
    cart_btn = wait.until(EC.presence_of_element_located(ShopHeader.CART_CONTAINER))
    
    assert cart_btn.is_displayed()

def test_main_sanity_products(driver:webdriver):
    """Test presence of specific products on main page"""
    driver.get(KIRILS_SHOP_URL)
    
    wait = WebDriverWait(driver, 20)
    landing_container = wait.until(
        EC.presence_of_element_located(LandingPage.LANDING_CONTAINER)
    )
    driver.execute_script("arguments[0].scrollIntoView(true);", landing_container)
    
    product_names = wait.until(
        EC.presence_of_all_elements_located(LandingPage.ALL_PRODUCTS_NAME)
    )
    product_texts = [product.text for product in product_names]
    
    expected_products = [
        'Radiant Tee', 'Breathe-Easy Tank', 'Argus All-Weather Tank',
        'Hero Hoodie', 'Fusion Backpack', 'Push It Messenger Bag'
    ]
    
    assert all(product in product_texts for product in expected_products)

def test_main_sanity_add_to_cart_hover(driver:webdriver):
    """Test 'Add to Cart' button appears on product hover"""
    driver.get(KIRILS_SHOP_URL)
    
    wait = WebDriverWait(driver, 20)
    products = wait.until(
        EC.presence_of_all_elements_located(LandingPage.ALL_PRODUCTS_PREVIEWS)
    )
    
    first_product = products[0]
    driver.execute_script("arguments[0].scrollIntoView(true);", first_product)
    
    actions = webdriver.ActionChains(driver)
    actions.move_to_element(first_product).perform()
    
    add_to_cart_btn = wait.until(
        EC.visibility_of_element_located(LandingPage.ALL_PRODUCTS_ADD_TO_CARD_BUTTONS)
    )
    
    assert add_to_cart_btn.is_displayed()

def test_main_positive_no_add_to_cart_without_hover(driver:webdriver):
    """Test 'Add to Cart' button is not visible without hover"""
    driver.get(KIRILS_SHOP_URL)
    
    wait = WebDriverWait(driver, 20)
    products = wait.until(
        EC.presence_of_all_elements_located(LandingPage.ALL_PRODUCTS_PREVIEWS)
    )
    
    first_product = products[0]
    driver.execute_script("arguments[0].scrollIntoView(true);", first_product)
    time.sleep(5)
    add_to_cart_btns = driver.find_elements(*LandingPage.ALL_PRODUCTS_ADD_TO_CARD_BUTTONS)
    for idx, btn in enumerate(add_to_cart_btns):
        print(idx)
        print(btn.is_displayed())
        assert not btn.is_displayed()
    # assert not any(btn.is_displayed() for btn in add_to_cart_btns)

def test_main_positive_search(driver:webdriver):
    """Test search functionality from main page"""
    driver.get(KIRILS_SHOP_URL)
    
    wait = WebDriverWait(driver, 20)
    search_bar = wait.until(EC.presence_of_element_located(ShopHeader.SEARCH_BAR))
    
    search_bar.send_keys('T shirt')
    search_bar.send_keys(Keys.RETURN)
    
    products_container = wait.until(
        EC.presence_of_element_located(ProductsPage.PRODUCTS_PAGE_CONTAINER)
    )
    products = wait.until(
        EC.presence_of_all_elements_located(ProductsPage.ALL_PRODUCTS)
    )
    
    assert products_container.is_displayed()
    assert len(products) >= 1

def test_main_negative_empty_search(driver:webdriver):
    """Test empty search keeps user on main page"""
    driver.get(KIRILS_SHOP_URL)
    
    wait = WebDriverWait(driver, 20)
    search_bar = wait.until(EC.presence_of_element_located(ShopHeader.SEARCH_BAR))
    
    search_bar.click()
    search_bar.send_keys(Keys.RETURN)
    
    landing_container = wait.until(
        EC.presence_of_element_located(LandingPage.LANDING_CONTAINER)
    )
    
    assert landing_container.is_displayed()

def test_main_boundary_search_input_limit(driver:webdriver):
    """Test search input character limit"""
    driver.get(KIRILS_SHOP_URL)
    
    wait = WebDriverWait(driver, 20)
    search_bar = wait.until(EC.presence_of_element_located(ShopHeader.SEARCH_BAR))
    
    long_input = 'a' * 130
    search_bar.send_keys(long_input)
    
    actual_input = search_bar.get_attribute('value')
    
    assert len(actual_input) == 128

def test_main_positive_category_navigation(driver:webdriver):
    """Test category navigation from main page"""
    driver.get(KIRILS_SHOP_URL)
    
    wait = WebDriverWait(driver, 20)
    men_category = wait.until(EC.presence_of_element_located(ShopHeader.MEN_CATEGORY))
    
    actions = webdriver.ActionChains(driver)
    actions.move_to_element(men_category).perform()
    
    tops_category = wait.until(
        EC.visibility_of_element_located(ShopHeader.MEN_CATEGORY_TOOL)
    )
    actions.move_to_element(tops_category).perform()
    
    tanks_category = wait.until(
        EC.visibility_of_element_located(ShopHeader.MEN_CATEGORY_TOOL_TANKS)
    )
    tanks_category.click()
    
    wait.until(EC.title_contains('Tanks'))
    
    products = wait.until(
        EC.presence_of_all_elements_located(ProductsPage.ALL_PRODUCTS)
    )
    
    assert 'Tanks' in driver.title
    assert len(products) == 12
    assert all('Tank' in product.text for product in products)
