
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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

@pytest.fixture
def shop_header(driver):
    """Fixture for ShopHeader page object model."""
    return ShopHeader(driver)

@pytest.fixture
def products_page(driver):
    """Fixture for ProductsPage page object model."""
    return ProductsPage(driver)

def test_price_filter_boundary_men_hoodies_sweatshirts(
    driver,
    shop_header,
    products_page
):
    """Test price filter boundary for men's hoodies and sweatshirts."""
    driver.get(KIRILS_SHOP_URL)

    # Hover over Men category
    men_category = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located(shop_header.men_category)
    )
    WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable(shop_header.men_category)
    )
    driver.execute_script("arguments[0].scrollIntoView();", men_category)
    driver.execute_script("arguments[0].hover();", men_category)

    # Click on "Hoodies & Sweatshirts" in the dropdown
    WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable(shop_header.all_hoodies_and_sweatshirts)
    ).click()

    # Wait for the products page to load
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located(products_page.products_page_container)
    )

    # Click on the price dropdown
    WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable(products_page.price_dropdown)
    ).click()

    # Select the $40-49.99 range
    WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable(products_page.range_40__49_99)
    ).click()

    # Wait for the page to update with filtered results
    WebDriverWait(driver, 20).until(
        EC.staleness_of(driver.find_element(*products_page.all_products[0]))
    )

    # Get all product prices
    price_elements = WebDriverWait(driver, 20).until(
        EC.presence_of_all_elements_located(products_page.all_product_prices)
    )

    # Check that no price is less than $40 or greater than $49.99
    for price_element in price_elements:
        price_text = price_element.text.strip('$')
        price = float(price_text)

        assert 40 <= price <= 49.99, (
            f'Price ${price} is outside the expected range of $40-$49.99'
        )