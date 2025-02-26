#test_saucedemo_2_page.py
import pytest
import logging
from sauce_lib import TestSauce
from selenium.webdriver.common.by import By

@pytest.fixture(scope="session")
def test_sauce():
    sauce = TestSauce()
    sauce.main_URL = "https://www.saucedemo.com"
    sauce.driver = sauce.driver_init(browser="chrome")  # Initialize WebDriver (or choose 'edge' if needed)
    sauce.item_wants_to_add = "Sauce Labs Backpack"
    sauce.inventory_items_details = []
    yield sauce  # Provide the TestSauce instance to the tests
    # Cleanup after the test session finishes
    if hasattr(sauce, 'driver'):
        sauce.driver.quit()

# Parametrize the test data here
@pytest.fixture(scope="session", params=TestSauce.read_test_data_from_excel("test_data.xlsx"), ids=lambda val:val['username'])
def test_data(request):
    try:
        return request.param
    except FileNotFoundError:
        print("test_data.xlsx not found!")
        pytest.fail("Test data file not found!")

# Parametrize the test data here
@pytest.fixture(scope="function", params=TestSauce.read_filling_form_test_data_from_excel("filling_form_data.xlsx"))
def filling_form_data(request):
    try:
        return request.param
    except FileNotFoundError:
        print("filling_form_data.xlsx not found!")
        pytest.fail("filling_form_data file not found!")

# Test Login Page using the shared test data from the fixture
def test_login_functionality(test_sauce, test_data):
    try:
        test_sauce.verify_login_page(test_data)
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
def test_end_to_end_checkout_process(test_sauce, test_data, filling_form_data):
    try:
        print("\nTest end-to-end process with given test data")
        print("\nSTEP 1: Test login functionality.")
        test_sauce.verify_login_page(test_data)
        if test_data['expected_result'] == "success":
            assert "inventory" in test_sauce.driver.current_url, "Login failed!"
            print(f"\nLogin test for {test_data['username']} has passed and redirected to Inventory page.")
            print("------------------------------------------------------")
            # Perform the rest of the steps
            print("STEP 2: Test for inventory page after successful login")
            test_sauce.verify_inventory_page_details()
            print("STEP 3: Test for add to cart page.")
            test_sauce.verify_add_item_to_cart()
            print("STEP 4: Test for cart page after adding item to cart.")
            test_sauce.verify_cart_page()
            print("STEP 5: Test for checkout process.")
            test_sauce.verify_proceed_to_checkout_continue_button(test_data, filling_form_data)
            print("STEP 6: Test for Logout process.")
            test_sauce.verify_logout()
        else:
            error_message = test_sauce.driver.find_element(By.CSS_SELECTOR, ".error-message-container")
            assert error_message.is_displayed(), "Error message not displayed"
            print(f"\nLogin test for {test_data['username']} failed due to {error_message.text}!")
            print(f"\nEnd-to-end test for {test_data['username']} is not possible due to {error_message.text}!")
    except Exception as exc:
        raise exc