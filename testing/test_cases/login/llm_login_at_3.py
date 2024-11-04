import time

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from testing.pomss.landing_page import LandingPage
from testing.pomss.login_page import LoginPage
from testing.pomss.shop_header import ShopHeader

import pytest

KIRILS_SHOP_URL = 'https://magento.softwaretestingboard.com/'  # Replace with actual URL
TIMEOUT = 20

@pytest.fixture(scope='function')
def driver():
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service
    chrome_driver_path = '/Users/kirilspodgalskis/Desktop/Test-AI-tomation/testing/tests/chromedriver'
    service = Service(executable_path=chrome_driver_path)
    driver = webdriver.Chrome(service=service)

    yield driver

    driver.quit()


def test_login_edge_case(driver):
    """Test login functionality with edge case of clearing cookies."""
    wait = WebDriverWait(driver, 20)
    
    # Step 1: Open main page
    driver.get(KIRILS_SHOP_URL)
    wait.until(EC.presence_of_element_located(LandingPage.landing_container))
    
    # Step 2: Click "Sign in" in header
    sign_in = wait.until(EC.element_to_be_clickable(ShopHeader.sign_in))
    sign_in.click()
    
    # Step 3-5: Enter credentials and sign in
    wait.until(EC.presence_of_element_located(LoginPage.login_page_container))
    email_input = wait.until(EC.element_to_be_clickable(LoginPage.email_input))
    email_input.send_keys('kirils.podgalskis@edu.rtu.lv')
    
    password_input = wait.until(
        EC.element_to_be_clickable(LoginPage.password_input)
    )
    password_input.send_keys('Password123')
    
    sign_in_button = wait.until(
        EC.element_to_be_clickable(LoginPage.sign_in_button)
    )
    sign_in_button.click()
    
    # Step 6: Verify main page is displayed after login
    wait.until(EC.presence_of_element_located(LandingPage.landing_container))
    
    # Step 7: Clear Cookies
    driver.delete_all_cookies()
    
    # Step 8: Refresh page
    driver.refresh()
    
    # Step 9: Verify "Sign in" button is visible
    wait.until(EC.presence_of_element_located(ShopHeader.sign_in))
    
    assert wait.until(
        EC.visibility_of_element_located(ShopHeader.sign_in)
    ), 'Sign in button is not visible after clearing cookies and refreshing'
