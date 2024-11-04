import time
from typing import List

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

## edited
from page_objects.landing_page import LandingPage
from page_objects.products_page import ProductsPage

## added
@pytest.fixture(scope="function")
def driver():
    # Setup Chrome options (you can also use other browsers like Firefox)
    chrome_driver_path = '/Users/kirilspodgalskis/Desktop/Test-AI-tomation/testing/tests/chromedriver'  # Pointing to the chromedriver in the current directory
    service = Service(executable_path=chrome_driver_path)
    driver = webdriver.Chrome(service=service)

    yield driver
    
    # Teardown (quit the browser after each test)
    driver.quit()
## added

@pytest.fixture(scope='module')
def landing_page(driver):
    """Fixture to return LandingPage instance."""
    return LandingPage(driver)


@pytest.fixture(scope='module')
def products_page(driver):
    """Fixture to return ProductsPage instance."""
    return ProductsPage(driver)


def test_main_page_sanity_buttons(driver, landing_page):
    """Test main page sanity: Sign In and Cart buttons visibility."""
    landing_page.open()
    
    assert WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located(landing_page.SIGN_IN)
    )
    assert WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located(landing_page.CART_CONTAINER)
    )


def test_main_page_sanity_product_cards(driver, landing_page):
    """Test main page sanity: visibility of specific product cards."""
    landing_page.open()
    driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
    
    expected_products = [
        'Radiant tee', 'Breate-Easy Tank', 'Argus All-Weather Tank',
        'Hero Hoodie', 'Fussion backpack', 'Push It Messenger Bag'
    ]
    
    product_names = WebDriverWait(driver, 20).until(
        EC.presence_of_all_elements_located(landing_page.ALL_PRODUCTS_NAME)
    )
    actual_products = [product.text for product in product_names]
    
    assert all(product in actual_products for product in expected_products)


def test_main_page_sanity_add_to_cart_hover(driver, landing_page):
    """Test main page sanity: 'Add to Cart' button visibility on hover."""
    landing_page.open()
    driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
    
    first_product = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located(landing_page.ALL_PRODUCTS_PREVIEWS)
    )
    
    # Check 'Add to Cart' not visible before hover
    add_to_cart_buttons = driver.find_elements(*landing_page.ALL_PRODUCTS_ADD_TO_CARD_BUTTONS)
    assert not any(button.is_displayed() for button in add_to_cart_buttons)
    
    # Hover and check 'Add to Cart' visibility
    driver.execute_script('arguments[0].scrollIntoView();', first_product)
    WebDriverWait(driver, 20).until(EC.visibility_of(first_product))
    driver.execute_script('arguments[0].dispatchEvent(new MouseEvent("mouseover", {bubbles: true}));', first_product)
    
    add_to_cart_button = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located(landing_page.ALL_PRODUCTS_ADD_TO_CARD_BUTTONS)
    )
    assert add_to_cart_button.is_displayed()
    
    # Move mouse away and check 'Add to Cart' not visible
    driver.execute_script('arguments[0].dispatchEvent(new MouseEvent("mouseout", {bubbles: true}));', first_product)
    time.sleep(1)  # Allow time for button to hide
    assert not add_to_cart_button.is_displayed()


def test_main_page_search_positive(driver, landing_page, products_page):
    """Test main page positive search: 'T shirt' query."""
    landing_page.open()
    
    search_bar = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable(landing_page.SEARCH_BAR)
    )
    search_bar.send_keys('T shirt')
    search_bar.send_keys(Keys.RETURN)
    
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located(products_page.PRODUCTS_PAGE_CONTAINER)
    )
    
    products = WebDriverWait(driver, 20).until(
        EC.presence_of_all_elements_located(products_page.ALL_PRODUCTS)
    )
    assert len(products) >= 1


def test_main_page_search_negative(driver, landing_page):
    """Test main page negative search: empty query."""
    landing_page.open()
    
    search_bar = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable(landing_page.SEARCH_BAR)
    )
    search_bar.click()
    search_bar.send_keys(Keys.RETURN)
    
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located(landing_page.LANDING_CONTAINER)
    )
    assert driver.current_url == landing_page.url


def test_main_page_search_boundary(driver, landing_page):
    """Test main page search boundary: 130 characters input."""
    landing_page.open()
    
    search_bar = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable(landing_page.SEARCH_BAR)
    )
    search_bar.click()
    
    long_input = 'a' * 130
    search_bar.send_keys(long_input)
    
    actual_input = search_bar.get_attribute('value')
    assert len(actual_input) == 128


def test_main_page_category_navigation(driver, landing_page, products_page):
    """Test main page category navigation: Men > Tops > Tanks."""
    landing_page.open()
    
    men_category = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable(landing_page.MEN_CATEGORY)
    )
    driver.execute_script('arguments[0].dispatchEvent(new MouseEvent("mouseover", {bubbles: true}));', men_category)
    
    tanks_category = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable(landing_page.MEN_CATEGORY_TOOL_TANKS)
    )
    tanks_category.click()
    
    WebDriverWait(driver, 20).until(
        EC.text_to_be_present_in_element(products_page.PRODUCTS_PAGE_CONTAINER, 'Tanks')
    )
    
    products = WebDriverWait(driver, 20).until(
        EC.presence_of_all_elements_located(products_page.ALL_PRODUCTS)
    )
    assert len(products) == 12
    
    product_names = WebDriverWait(driver, 20).until(
        EC.presence_of_all_elements_located(products_page.ALL_PRODUCTS)
    )
    assert all('Tank' in product.text for product in product_names)