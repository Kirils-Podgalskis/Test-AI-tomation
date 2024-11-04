
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from testing.pomss.login_page import LoginPage
from testing.pomss.shop_header import ShopHeader
from testing.pomss.account_page import AccountPage

import pytest

KIRILS_SHOP_URL = 'https://magento.softwaretestingboard.com/'

@pytest.fixture(scope='function')
def driver():
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service
    chrome_driver_path = '/Users/kirilspodgalskis/Desktop/Test-AI-tomation/testing/tests/chromedriver'
    service = Service(executable_path=chrome_driver_path)
    driver = webdriver.Chrome(service=service)

    yield driver

    driver.quit()

def test_login_page_sanity(driver):
    """Test case N1: Login page Sanity"""
    driver.get(KIRILS_SHOP_URL)
    
    header = ShopHeader(driver)
    header.sign_in.click() #
    
    login_page = LoginPage(driver)
    assert login_page.email_input.is_displayed() # 
    assert login_page.password_input.is_displayed() #
    assert login_page.sign_in_button.is_displayed() #

def test_login_page_negative_empty_fields(driver):
    """Test case N2: Login page Negative - Empty fields"""
    driver.get(KIRILS_SHOP_URL)
    
    header = ShopHeader(driver)
    header.sign_in.click() #
    
    login_page = LoginPage(driver)
    assert 'Sign in' in login_page.login_page_container.text
    
    login_page.sign_in_button.click() #
    
    assert 'This is a required field' in login_page.email_input_error.text #
    assert 'This is a required field' in login_page.password_input_error.text #

def test_login_page_negative_incorrect_credentials(driver):
    """Test case N3: Login page Negative - Incorrect credentials"""
    driver.get(KIRILS_SHOP_URL)
    
    header = ShopHeader(driver)
    header.sign_in.click() #
    
    login_page = LoginPage(driver)
    login_page.email_input.send_keys('kirils.podgalskis@edu.rtu.lv') #
    login_page.password_input.send_keys('incorrect') #
    login_page.sign_in_button.click() #
    
    error_message = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, '.message-error'))
    )
    assert 'The account sign-in was incorrect or your account is disabled temporarily.' in error_message.text

def test_login_page_positive(driver):
    """Test case N4: Login page Positive"""
    driver.get(KIRILS_SHOP_URL)
    
    header = ShopHeader(driver)
    header.sign_in.click() #
    
    login_page = LoginPage(driver)
    login_page.email_input.send_keys('kirils.podgalskis@edu.rtu.lv') #
    login_page.password_input.send_keys('Password123') #
    login_page.sign_in_button.click() #
    
    account_page = AccountPage(driver)
    assert account_page.my_account_page.is_displayed() #

def test_login_page_edge_case_clear_cookies(driver):
    """Test case N5: Login page Edge case - Clear cookies"""
    driver.get(KIRILS_SHOP_URL)
    
    header = ShopHeader(driver)
    header.sign_in.click() #
    
    login_page = LoginPage(driver)
    login_page.email_input.send_keys('kirils.podgalskis@edu.rtu.lv') #
    login_page.password_input.send_keys('Password123') #
    login_page.sign_in_button.click() #
    
    account_page = AccountPage(driver)
    assert account_page.my_account_page.is_displayed() #
    
    driver.delete_all_cookies()
    driver.refresh()
    
    try:
        WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located(login_page.login_page_container)
        )
    except TimeoutException:
        assert False, "Login page did not appear after clearing cookies and refreshing"

def test_login_page_negative_invalid_email(driver):
    """Test case N6: Login page Negative - Invalid email"""
    driver.get(KIRILS_SHOP_URL)
    
    header = ShopHeader(driver)
    header.sign_in.click() #
    
    login_page = LoginPage(driver)
    login_page.email_input.send_keys('kirils.podgalskis') #
    login_page.password_input.send_keys('Password123') #
    login_page.sign_in_button.click() #
    
    assert 'Please enter a valid email address (Ex: johndoe@domain.com).' in login_page.email_input_error.text

def test_login_page_security_sql_injection(driver):
    """Test case N7: Login page Security - SQL injection"""
    driver.get(KIRILS_SHOP_URL)
    
    header = ShopHeader(driver)
    header.sign_in.click() #
    
    login_page = LoginPage(driver)
    login_page.email_input.send_keys('kirils.podgalskis@edu.rtu.lv') #
    login_page.password_input.send_keys("' OR '1'='1") #
    login_page.sign_in_button.click() #
    
    error_message = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, '.message-error'))
    )
    assert 'The account sign-in was incorrect or your account is disabled temporarily.' in error_message.text