import pytest
import os
from decimal import Decimal

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from testing.pomss.landing_page import LandingPage

@pytest.fixture(scope="function")
def driver():
    # Setup Chrome options (you can also use other browsers like Firefox)
    chrome_driver_path = '/Users/kirilspodgalskis/Desktop/Test-AI-tomation/testing/tests/chromedriver'  # Pointing to the chromedriver in the current directory
    service = Service(executable_path=chrome_driver_path)
    driver = webdriver.Chrome(service=service)

    yield driver
    
    # Teardown (quit the browser after each test)
    driver.quit()

# def test_landing_container_visible(driver:webdriver):
#     """Test boundary condition for product search by price"""
#     driver.get("https://magento.softwaretestingboard.com/")
    
#     # Initialize the MainPage object
#     main_page = LandingPage(driver)
    
#     # Wait for the LANDING_CONTAINER to be visible
#     WebDriverWait(driver, 10).until(
#         EC.visibility_of_element_located(main_page.LANDING_CONTAINER)
#     )
    
#     # Assert that the landing container is displayed
#     landing_container = driver.find_element(*main_page.LANDING_CONTAINER)
#     assert landing_container.is_displayed(), "Landing container is not visible"

@pytest.mark.sanity
def test_sign_in_button_visible_landing_sanity(driver):
    """Verify SIGN IN button is visible on the landing page."""
    main_page = LandingPage(driver)
    driver.get('https://magento.softwaretestingboard.com/')

    WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located(main_page.LANDING_CONTAINER)
    )

    assert WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located(main_page.SIGN_IN)
    ), 'SIGN IN button is not visible on the landing page'