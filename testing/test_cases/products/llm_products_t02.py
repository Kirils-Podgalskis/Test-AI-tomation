import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

from testing.pomss.shop_header import ShopHeader
from testing.pomss.products_page import ProductsPage

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

@pytest.fixture
def shop_header(driver):
    """Fixture for ShopHeader page object model."""
    return ShopHeader(driver)


@pytest.fixture
def products_page(driver):
    """Fixture for ProductsPage page object model."""
    return ProductsPage(driver)


def test_price_filter_boundary_products_page(driver, shop_header, products_page):
    """Test price filter boundary on products page."""
    driver.get(KIRILS_SHOP_URL)

    # Hover over Men category and click on Hoodies & Sweatshirts
    men_category = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable(shop_header.men_category)
    )
    ActionChains(driver).move_to_element(men_category).perform()
    
    hoodies_link = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable(shop_header.all_hoodies_and_sweatshirts)
    )
    hoodies_link.click()

    # Wait for products page to load
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located(products_page.products_page_container)
    )

    # Click on price dropdown and select $40-49.99 range
    price_dropdown = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable(products_page.price_dropdown)
    )
    price_dropdown.click()

    price_range = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable(products_page.range_40__49_99)
    )
    price_range.click()

    # Wait for products to be updated
    WebDriverWait(driver, 20).until(
        EC.staleness_of(driver.find_element(*products_page.all_products[0]))
    )

    # Get all product prices
    product_prices = WebDriverWait(driver, 20).until(
        EC.presence_of_all_elements_located(products_page.all_product_prices)
    )

    # Check that all prices are within the selected range
    for price_element in product_prices:
        price_text = price_element.text.strip('$')
        price = float(price_text)
        
        assert 40 <= price <= 49.99, f'Price {price} is out of range $40-$49.99'