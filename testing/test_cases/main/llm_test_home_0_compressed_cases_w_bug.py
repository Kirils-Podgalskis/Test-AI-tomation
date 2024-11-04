import time

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

## 3 lines fixed
from testing.pomss.landing_page import LandingPage
from testing.pomss.shop_header import ShopHeader
from testing.pomss.products_page import ProductsPage

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

def test_main_page_sanity_sign_in_cart(driver):
    """Test presence of Sign In and Cart buttons on main page."""
    driver.get(KIRILS_SHOP_URL)
    wait = WebDriverWait(driver, TIMEOUT)

    sign_in = wait.until(EC.presence_of_element_located(ShopHeader.SIGN_IN))
    cart = wait.until(EC.presence_of_element_located(ShopHeader.CART_CONTAINER))

    assert sign_in.is_displayed()
    assert cart.is_displayed()

def test_main_page_sanity_product_cards(driver):
    """Test presence of specific product cards on main page."""
    driver.get(KIRILS_SHOP_URL)
    wait = WebDriverWait(driver, TIMEOUT)

    products = wait.until(
        EC.presence_of_all_elements_located(LandingPage.ALL_PRODUCTS_NAME)
    )
    product_names = [p.text for p in products]

    expected_products = [
        'Radiant Tee', 'Breathe-Easy Tank', 'Argus All-Weather Tank',
        'Hero Hoodie', 'Fusion Backpack', 'Push It Messenger Bag'
    ]

    for product in expected_products:
        assert product in product_names, f'{product} not found on main page'

def test_main_page_sanity_add_to_cart_hover(driver):
    """Test 'Add to Cart' button visibility on product card hover."""
    driver.get(KIRILS_SHOP_URL)
    wait = WebDriverWait(driver, TIMEOUT)

    first_product = wait.until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, f'{LandingPage.ALL_PRODUCTS_PREVIEWS[1]} > li:first-child')
        )
    )
    add_to_cart_button = first_product.find_element(*LandingPage.ALL_PRODUCTS_ADD_TO_CARD_BUTTONS)

    assert not add_to_cart_button.is_displayed()

    webdriver.ActionChains(driver).move_to_element(first_product).perform()
    time.sleep(0.5)  # Short delay to ensure hover effect is applied

    assert add_to_cart_button.is_displayed()

def test_main_page_positive_search(driver):
    """Test search functionality from main page."""
    driver.get(KIRILS_SHOP_URL)
    wait = WebDriverWait(driver, TIMEOUT)

    search_bar = wait.until(EC.presence_of_element_located(ShopHeader.SEARCH_BAR))
    search_bar.send_keys('T shirt')
    search_bar.send_keys(Keys.RETURN)

    products_container = wait.until(
        EC.presence_of_element_located(ProductsPage.PRODUCTS_PAGE_CONTAINER)
    )
    products = products_container.find_elements(*ProductsPage.ALL_PRODUCTS)

    assert len(products) > 0, 'No search results found for "T shirt"'

def test_main_page_negative_empty_search(driver):
    """Test empty search from main page."""
    driver.get(KIRILS_SHOP_URL)
    wait = WebDriverWait(driver, TIMEOUT)

    search_bar = wait.until(EC.presence_of_element_located(ShopHeader.SEARCH_BAR))
    search_bar.send_keys(Keys.RETURN)

    landing_container = wait.until(
        EC.presence_of_element_located(LandingPage.LANDING_CONTAINER)
    )

    assert landing_container.is_displayed(), 'Main page not displayed after empty search'

def test_main_page_boundary_search_input(driver):
    """Test search input character limit."""
    driver.get(KIRILS_SHOP_URL)
    wait = WebDriverWait(driver, TIMEOUT)

    search_bar = wait.until(EC.presence_of_element_located(ShopHeader.SEARCH_BAR))
    long_input = 'a' * 130
    search_bar.send_keys(long_input)

    actual_input = search_bar.get_attribute('value')

    assert len(actual_input) == 128, f'Search bar accepts {len(actual_input)} chars, expected 128'

def test_main_page_positive_category_navigation(driver):
    """Test category navigation from main page."""
    driver.get(KIRILS_SHOP_URL)
    wait = WebDriverWait(driver, TIMEOUT)

    men_category = wait.until(EC.presence_of_element_located(ShopHeader.MEN_CATEGORY))
    webdriver.ActionChains(driver).move_to_element(men_category).perform()

    tops_category = wait.until(EC.presence_of_element_located(ShopHeader.MEN_CATEGORY_TOOL))
    webdriver.ActionChains(driver).move_to_element(tops_category).perform()

    tanks_category = wait.until(
        EC.element_to_be_clickable(ShopHeader.MEN_CATEGORY_TOOL_TANKS)
    )
    tanks_category.click()

    products_title = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '.page-title'))
    )
    assert 'Tanks' in products_title.text

    products = wait.until(
        EC.presence_of_all_elements_located(ProductsPage.ALL_PRODUCTS)
    )
    assert len(products) == 12, f'Expected 12 tank products, found {len(products)}'

    for product in products:
        assert 'Tank' in product.text, f'Product "{product.text}" does not contain "Tank"'