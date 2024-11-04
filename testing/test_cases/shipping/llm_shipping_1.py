
import time
from datetime import datetime
import random

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select

from testing.pomss.landing_page import LandingPage
from testing.pomss.shopping_cart_page import ShoppingCartPage
from testing.pomss.shipping_page import ShippingPage
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

def test_shipping_page_positive(driver):
    """
    Test positive flow for shipping page
    """
    landing_page = LandingPage(driver)
    shopping_cart_page = ShoppingCartPage(driver)
    shipping_page = ShippingPage(driver)

    # 1. Open main page
    driver.get(KIRILS_SHOP_URL)

    # 2. Scroll down
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # 3. Add Fusion backpack to cart
    fusion_backpack = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable(landing_page.fusion_backpack_preview)
    )
    fusion_backpack.click()

    add_to_cart_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.action.tocart.primary'))
    )
    add_to_cart_button.click()

    # 4. See: "You added Fusion Backpack to your shopping cart."
    WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, 'div.message-success'))
    )

    # 5. Click "shopping cart" in success banner
    shopping_cart_link = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.LINK_TEXT, 'shopping cart'))
    )
    shopping_cart_link.click()

    # 6. Click "Proceed to checkout"
    WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable(shopping_cart_page.proceed_to_checkout)
    ).click()

    # 7. See Shipping page
    WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located(shipping_page.shipping_page_container)
    )

    # 8. Enter email
    current_time = datetime.now().strftime("%d_%H_%M_%S")
    random_digits = ''.join([str(random.randint(0, 9)) for _ in range(4)])
    email = f'kirils.podgalskis+{current_time}_{random_digits}@edu.rtu.lv'
    
    email_input = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located(shipping_page.email_input)
    )
    email_input.send_keys(email)

    # 9. No "Enter password" after 15s
    time.sleep(15)
    # password_input = driver.find_elements(*shipping_page.password_input)
    WebDriverWait(driver, 20).until(
        EC.invisibility_of_element_located(shipping_page.password_input)
    )
    # assert len(password_input) == 0, "Password input appeared unexpectedly"

    # 10-12. Enter First name, Last name, and Address
    WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located(shipping_page.first_name_input)
    ).send_keys('Kirils')

    driver.find_element(By.NAME, 'lastname').send_keys('Podgaļskis')
    
    WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located(shipping_page.street_input)
    ).send_keys('Zunda krastmala 10')

    # 13-14. Select country and state
    country_select = Select(WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located(shipping_page.country_select)
    ))
    country_select.select_by_visible_text('Latvia')

    state_select = Select(WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located(shipping_page.state_provice_select)
    ))
    state_select.select_by_visible_text('Rīga')

    # 15-17. Enter city, zip, and phone
    WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located(shipping_page.city_input)
    ).send_keys('Rīga')

    WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located(shipping_page.zip_pastcode_input)
    ).send_keys('1048')

    WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located(shipping_page.phone_number)
    ).send_keys('67089333')

    time.sleep(10)
    # 18. Click Next
    WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable(shipping_page.next_button)
    ).click()

    time.sleep(2)
    # 19. Click "place order"
    WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable(shipping_page.place_order_button)
    ).click()

    
    # 20. See "Thank you for your purchase!"
    WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.XPATH, "//*[contains(text(), 'Thank you for your purchase!')]"))
    )

    # 21. See "Your order # is: <order_number>" (digits)
    order_number_element = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located(shipping_page.order_number_label)
    )
    order_number_text = order_number_element.text

    assert 'Your order # is:' in order_number_text
    order_number = order_number_text.split(':')[-1].strip()
    assert order_number.isdigit(), f"Order number {order_number} is not a digit"