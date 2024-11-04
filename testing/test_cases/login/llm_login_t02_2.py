import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException

from testing.pomss.shop_header import ShopHeader
from testing.pomss.login_page import LoginPage
from testing.pomss.account_page import AccountPage
from testing.pomss.landing_page import LandingPage

import pytest

KIRILS_SHOP_URL = 'https://magento.softwaretestingboard.com/'

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

VALID_EMAIL = 'kirils.podgalskis@edu.rtu.lv'
VALID_PASSWORD = 'Password123'
INVALID_PASSWORD = 'incorrect'
INVALID_EMAIL = 'kirils.podgalskis'
SQL_INJECTION = "' OR '1'='1"

def test_login_page_sanity(driver):
    """Test case N1: Login page Sanity"""
    driver.get(KIRILS_SHOP_URL)
    
    header = ShopHeader(driver)
    login_page = LoginPage(driver)
    
    WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable(header.sign_in)
    ).click()
    
    WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located(login_page.email_input)
    )
    WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located(login_page.password_input)
    )
    WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable(login_page.sign_in_button)
    )

def test_login_page_negative_empty_fields(driver):
    """Test case N2: Login page Negative - Empty fields"""
    driver.get(KIRILS_SHOP_URL)
    
    header = ShopHeader(driver)
    login_page = LoginPage(driver)
    
    WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable(header.sign_in)
    ).click()

    
    WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable(login_page.sign_in_button)
    ).click()
    
    WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located(login_page.email_input_error)
    )
    WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located(login_page.password_input_error)
    )
    
    assert driver.find_element(*login_page.email_input_error).text == (
        'This is a required field.'
    )
    assert driver.find_element(*login_page.password_input_error).text == (
        'This is a required field.'
    )

def test_login_page_negative_incorrect_password(driver):
    """Test case N3: Login page Negative - Incorrect password"""
    driver.get(KIRILS_SHOP_URL)
    
    header = ShopHeader(driver)
    login_page = LoginPage(driver)
    
    WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable(header.sign_in)
    ).click()
    
    WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located(login_page.email_input)
    ).send_keys(VALID_EMAIL)
    
    WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located(login_page.password_input)
    ).send_keys(INVALID_PASSWORD)
    
    WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable(login_page.sign_in_button)
    ).click()
    
    error_message = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located(
            (By.XPATH, "//div[contains(@class, 'message-error')]")
        )
    )
    
    assert error_message.text == (
        'The account sign-in was incorrect or your account is disabled '
        'temporarily. Please wait and try again later.'
    )

def test_login_page_positive(driver):
    """Test case N4: Login page Positive"""
    driver.get(KIRILS_SHOP_URL)
    
    header = ShopHeader(driver)
    login_page = LoginPage(driver)
    account_page = AccountPage(driver)
    
    WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable(header.sign_in)
    ).click()
    
    WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located(login_page.email_input)
    ).send_keys(VALID_EMAIL)
    
    WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located(login_page.password_input)
    ).send_keys(VALID_PASSWORD)
    
    WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable(login_page.sign_in_button)
    ).click()
    
    WebDriverWait(driver, 20).until(
        EC.invisibility_of_element(header.sign_in)
    )

def test_login_page_edge_case_clear_cookies(driver):
    """Test case N5: Login page Edge case - Clear cookies"""
    driver.get(KIRILS_SHOP_URL)
    
    header = ShopHeader(driver)
    login_page = LoginPage(driver)
    account_page = AccountPage(driver)
    landing_page = LandingPage(driver)
    
    WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable(header.sign_in)
    ).click()
    
    WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located(login_page.email_input)
    ).send_keys(VALID_EMAIL)
    
    WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located(login_page.password_input)
    ).send_keys(VALID_PASSWORD)
    
    WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable(login_page.sign_in_button)
    ).click()
    
    WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located(landing_page.landing_container)
    )
    
    driver.delete_all_cookies()
    driver.refresh()
    
    WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located(landing_page.landing_container)
    )

def test_login_page_negative_invalid_email(driver):
    """Test case N6: Login page Negative - Invalid email"""
    driver.get(KIRILS_SHOP_URL)
    
    header = ShopHeader(driver)
    login_page = LoginPage(driver)
    
    WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable(header.sign_in)
    ).click()
    
    WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located(login_page.email_input)
    ).send_keys(INVALID_EMAIL)
    
    WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located(login_page.password_input)
    ).send_keys(VALID_PASSWORD)
    
    WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable(login_page.sign_in_button)
    ).click()
    
    error_message = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located(login_page.email_input_error)
    )
    
    assert error_message.text == (
        'Please enter a valid email address (Ex: johndoe@domain.com).'
    )

def test_login_page_security_sql_injection(driver):
    """Test case N7: Login page Security - SQL injection"""
    driver.get(KIRILS_SHOP_URL)
    
    header = ShopHeader(driver)
    login_page = LoginPage(driver)
    
    WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable(header.sign_in)
    ).click()
    
    WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located(login_page.email_input)
    ).send_keys(VALID_EMAIL)
    
    WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located(login_page.password_input)
    ).send_keys(SQL_INJECTION)
    
    WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable(login_page.sign_in_button)
    ).click()
    
    error_message = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located(
            (By.XPATH, "//*[contains(@class, 'message-error')]")
        )
    )
    
    assert error_message.text == (
        'The account sign-in was incorrect or your account is disabled '
        'temporarily. Please wait and try again later.'
    )