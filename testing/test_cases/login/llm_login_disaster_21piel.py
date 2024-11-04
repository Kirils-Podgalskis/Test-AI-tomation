import pytest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium import webdriver


from testing.pomss.shop_header import ShopHeader
from testing.pomss.login_page import LoginPage
from testing.pomss.account_page import AccountPage

KIRILS_SHOP_URL = 'https://magento.softwaretestingboard.com/'
EMAIL = 'kirils.podgalskis@edu.rtu.lv'
PASSWORD = 'Password123'
SQL_INJECTION = "' OR '1'='1"


@pytest.fixture(scope="function")
def driver():
    chrome_driver_path = '/Users/kirilspodgalskis/Desktop/Test-AI-tomation/testing/tests/chromedriver'
    service = Service(executable_path=chrome_driver_path)
    options = Options()
    options.add_extension('/Users/kirilspodgalskis/Desktop/Test-AI-tomation/testing/tests/CJPALHDLNBPAFIAMEJDNHCPHJBKEIAGM_1_60_0_0.crx')
    driver = webdriver.Chrome(service=service, options=options)

    yield driver

    driver.quit()


def test_login_page_sanity_test(driver):
    """Test case N1: Login page Sanity"""
    driver.get(KIRILS_SHOP_URL)
    
    header = ShopHeader(driver)
    header.sign_in.click()
    
    login_page = LoginPage(driver)
    
    assert login_page.email_input.is_displayed()
    assert login_page.password_input.is_displayed()
    assert login_page.sign_in_button.is_displayed()


def test_login_page_negative_test_empty_fields(driver):
    """Test case N2: Login page Negative - Empty fields"""
    driver.get(KIRILS_SHOP_URL)
    
    header = ShopHeader(driver)
    header.sign_in.click()
    
    login_page = LoginPage(driver)
    assert 'Sign in' in login_page.login_page_container.text
    
    login_page.sign_in_button.click()
    
    assert 'This is a required field' in login_page.email_input_error.text
    assert 'This is a required field' in login_page.password_input_error.text


def test_login_page_negative_test_incorrect_credentials(driver):
    """Test case N3: Login page Negative - Incorrect credentials"""
    driver.get(KIRILS_SHOP_URL)
    
    header = ShopHeader(driver)
    header.sign_in.click()
    
    login_page = LoginPage(driver)
    login_page.email_input.send_keys(EMAIL)
    login_page.password_input.send_keys('incorrect')
    login_page.sign_in_button.click()
    
    error_message = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, '.message-error'))
    )
    
    assert ('The account sign-in was incorrect or your account is disabled '
            'temporarily. Please wait and try again later.') in error_message.text


def test_login_page_positive_test(driver):
    """Test case N4: Login page Positive"""
    driver.get(KIRILS_SHOP_URL)
    
    header = ShopHeader(driver)
    header.sign_in.click()
    
    login_page = LoginPage(driver)
    login_page.email_input.send_keys(EMAIL)
    login_page.password_input.send_keys(PASSWORD)
    login_page.sign_in_button.click()
    
    account_page = AccountPage(driver)
    
    assert account_page.my_account_page.is_displayed()


def test_login_page_edge_case_test(driver):
    """Test case N5: Login page Edge case - Clear cookies"""
    driver.get(KIRILS_SHOP_URL)
    
    header = ShopHeader(driver)
    header.sign_in.click()
    
    login_page = LoginPage(driver)
    login_page.email_input.send_keys(EMAIL)
    login_page.password_input.send_keys(PASSWORD)
    login_page.sign_in_button.click()
    
    account_page = AccountPage(driver)
    assert account_page.my_account_page.is_displayed()
    
    driver.delete_all_cookies()
    driver.refresh()
    
    assert login_page.login_page_container.is_displayed()


def test_login_page_negative_test_invalid_email(driver):
    """Test case N6: Login page Negative - Invalid email"""
    driver.get(KIRILS_SHOP_URL)
    
    header = ShopHeader(driver)
    header.sign_in.click()
    
    login_page = LoginPage(driver)
    login_page.email_input.send_keys('kirils.podgalskis')
    login_page.password_input.send_keys(PASSWORD)
    login_page.sign_in_button.click()
    
    assert ('Please enter a valid email address (Ex: johndoe@domain.com).' 
            in login_page.email_input_error.text)


def test_login_page_security_test(driver):
    """Test case N7: Login page Security - SQL injection"""
    driver.get(KIRILS_SHOP_URL)
    
    header = ShopHeader(driver)
    header.sign_in.click()
    
    login_page = LoginPage(driver)
    login_page.email_input.send_keys(EMAIL)
    login_page.password_input.send_keys(SQL_INJECTION)
    login_page.sign_in_button.click()
    
    error_message = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, '.message-error'))
    )
    
    assert ('The account sign-in was incorrect or your account is disabled '
            'temporarily. Please wait and try again later.') in error_message.text