#test_saucedemo_2_page.py
"""Description: this script will enter into website:https://www.saucedemo.com/ and do front-end E2E tests using Selenium
framework.
There are two main below test conducted using pytest and with shared test data( stored in "test_data.xlsx") from the
fixture where all users information added.

1. Test Login page functionality.
2. Test End-to-End Process functionality which is all page test activities shown step by step as below.
STEP 1: Test for login functionality.
STEP 2: Test for inventory page after successful login.
STEP 3: Test for add an item to the cart page.
STEP 4: Test for cart page after adding item to cart.
STEP 5: Test for checkout process.
STEP 6: Test for Logout process.
"""

import pytest
from sauce_lib import TestSauce
from selenium.webdriver.common.by import By

@pytest.fixture(scope="function")
def test_sauce():
    sauce = TestSauce()
    # sauce.main_URL = "https://www.saucedemo.com"
    sauce.driver = sauce.driver_init(browser="chrome")  # Initialize WebDriver (or choose 'edge' if needed)
    sauce.item_wants_to_add = "Sauce Labs Backpack"
    sauce.inventory_items_details = []
    yield sauce  # Provide the TestSauce instance to the tests
    # Cleanup after the test session finishes
    if hasattr(sauce, 'driver'):
        sauce.driver.quit()

# Parametrize the test data here
@pytest.fixture(scope="function", params=TestSauce.read_test_data_from_excel("test_data.xlsx"), ids=lambda val:val['username'])
def test_data(request):
    try:
        return request.param
    except FileNotFoundError:
        print("test_data.xlsx not found!")
        pytest.fail("Test data file not found!")

# Test Login Page using the shared test data from the fixture
def test_login_functionality(test_sauce, test_data, base_url):
    try:
        test_sauce.verify_login_page(test_data, base_url)
        if test_data['expected_result'] == "success":
            assert "inventory" in test_sauce.driver.current_url, "Login failed!"
            print(f"\nLogin test for {test_data['username']} passed!")
        elif test_data['expected_result'] == "error":
            error_message = test_sauce.driver.find_element(By.CSS_SELECTOR, ".error-message-container")
            assert error_message.is_displayed(), "Error message not displayed"
            print(f"\nLogin test for {test_data['username']} failed due to {error_message.text}!")
            print("------------------------------------------------------")
    except Exception as exc:
        print(f"Error in test_login_page: {exc}")
        raise exc

# Test End-to-End Process using the shared test data from the fixture
def test_end_to_end_checkout_process(test_sauce, test_data, base_url):
    try:
        print("\nTest end-to-end process with given test data")
        print("\nSTEP 1: Test login functionality.")
        test_sauce.verify_login_page(test_data, base_url)
        if test_data['expected_result'] == "success":
            assert "inventory" in test_sauce.driver.current_url, "Login failed!"
            print(f"\nLogin test for {test_data['username']} has passed and redirected to Inventory page.")
            print("------------------------------------------------------")
            # Perform the rest of the steps
            print("STEP 2: Test for inventory page after successful login")
            test_sauce.verify_inventory_page_details(base_url)
            print("STEP 3: Test for add an item to the cart page.")
            test_sauce.verify_add_item_to_cart(base_url)
            print("STEP 4: Test for cart page after adding item to cart.")
            test_sauce.verify_cart_page(base_url)
            print("STEP 5: Test for checkout process.")
            test_sauce.verify_proceed_to_checkout_continue_button(test_data,base_url)
            print("STEP 6: Test for Logout process.")
            test_sauce.verify_logout(base_url)
        else:
            error_message = test_sauce.driver.find_element(By.CSS_SELECTOR, ".error-message-container")
            assert error_message.is_displayed(), "Error message not displayed"
            print(f"\nLogin test for {test_data['username']} failed due to {error_message.text}!")
            print(f"\nEnd-to-end test for {test_data['username']} is not possible due to {error_message.text}!")
    except Exception as exc:
        raise exc
