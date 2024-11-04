import time




from selenium import webdriver
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

def test_main_page_sanity_and_functionality(driver):
    driver.get(KIRILS_SHOP_URL)
    
    wait = WebDriverWait(driver, 20)
    landing_page = LandingPage(driver)
    shop_header = ShopHeader(driver)
    
    # Check Sign In button
    sign_in_btn = wait.until(EC.visibility_of_element_located(shop_header.sign_in))
    assert sign_in_btn.is_displayed(), 'Sign In button not visible'
    
    # Check Cart button
    cart_btn = wait.until(EC.visibility_of_element_located(shop_header.cart_container))
    assert cart_btn.is_displayed(), 'Cart button not visible'
    
    # Scroll to bottom and check products
    driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
    time.sleep(1)  # Allow time for products to load
    
    expected_products = [
        'Radiant Tee', 'Breathe-Easy Tank', 'Argus All-Weather Tank',
        'Hero Hoodie', 'Fusion Backpack', 'Push It Messenger Bag'
    ]
    product_names = wait.until(
        EC.presence_of_all_elements_located(landing_page.all_products_name)
    )
    actual_products = [product.text for product in product_names]
    
    assert all(product in actual_products for product in expected_products), (
        'Not all expected products are present'
    )
    
    # Check "Add to Cart" button visibility on hover
    first_product = wait.until(
        EC.presence_of_element_located(landing_page.all_products_previews)
    )
    driver.execute_script('arguments[0].scrollIntoView();', first_product)
    
    add_to_cart_buttons = wait.until(
        EC.presence_of_all_elements_located(
            landing_page.all_products_add_to_card_buttons
        )
    )
    
    # Hover over first product
    webdriver.ActionChains(driver).move_to_element(first_product).perform()
    time.sleep(1)  # Allow time for hover effect
    
    assert add_to_cart_buttons[0].is_displayed(), (
        '"Add to Cart" button not visible on hover'
    )
    
    # Move mouse away and check button invisibility
    webdriver.ActionChains(driver).move_by_offset(0, -100).perform()
    time.sleep(1)  # Allow time for hover effect to disappear
    
    assert not add_to_cart_buttons[0].is_displayed(), (
        '"Add to Cart" button visible without hover'
    )
    
    # Test search functionality
    search_input = wait.until(EC.visibility_of_element_located(shop_header.search_bar))
    search_input.send_keys('T shirt')
    search_input.send_keys(Keys.RETURN)
    
    products_page = ProductsPage(driver)
    wait.until(EC.url_contains('catalogsearch/result'))
    
    search_results = wait.until(
        EC.presence_of_all_elements_located(products_page.all_products)
    )
    assert len(search_results) > 0, 'No search results found'
    
    # Test empty search
    driver.get(KIRILS_SHOP_URL)
    search_input = wait.until(EC.visibility_of_element_located(shop_header.search_bar))
    search_input.click()
    search_input.send_keys(Keys.RETURN)
    
    assert driver.current_url == KIRILS_SHOP_URL, 'Redirected from main page on empty search'
    
    # Test search input character limit
    long_input = 'a' * 130
    search_input.send_keys(long_input)
    actual_input = search_input.get_attribute('value')
    
    assert len(actual_input) == 128, f'Search input not limited to 128 characters: {len(actual_input)}'
    
    # Test category navigation
    men_category = wait.until(EC.visibility_of_element_located(shop_header.men_category))
    webdriver.ActionChains(driver).move_to_element(men_category).perform()
    
    tops_category = wait.until(EC.visibility_of_element_located(shop_header.men_category_tool))
    webdriver.ActionChains(driver).move_to_element(tops_category).perform()
    
    tanks_category = wait.until(
        EC.element_to_be_clickable(shop_header.men_category_tool_tanks)
    )
    tanks_category.click()
    
    wait.until(EC.url_contains('men/tops-men/tanks-men.html'))
    
    page_title = driver.title
    assert 'Tanks' in page_title, f'Tanks not in page title: {page_title}'
    
    tank_products = wait.until(
        EC.presence_of_all_elements_located(products_page.all_products)
    )
    assert len(tank_products) == 12, f'Expected 12 tank products, found {len(tank_products)}'
    