#sauce_lib.py
import pytest
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

class TestSauce:

    @staticmethod
    def driver_init(browser="chrome"):
        """Initialize the web driver with the given browser (chrome/edge)."""
        if browser == "edge":
            driver = webdriver.Edge(service=Service(EdgeDriverManager().install()))
        elif browser == "chrome":
            options = Options()
            options.add_argument("start-maximized")
            driver = webdriver.Chrome(
                service=Service(ChromeDriverManager().install()), options=options
            )
        else:
            raise AttributeError(f"Web driver {browser} not found")
        return driver

    @staticmethod
    # Function to read test data from Excel file
    def read_test_data_from_excel(file_path):
        # Read the Excel file into a pandas DataFrame
        df = pd.read_excel(file_path)
        # Return the data as a list of dictionaries (row-by-row)
        return df.to_dict(orient="records")

    @staticmethod
    # Function to read test data from Excel file
    def read_filling_form_test_data_from_excel(file_path):
        # Read the Excel file into a pandas DataFrame
        df = pd.read_excel(file_path)
        # Return the data as a list of dictionaries (row-by-row)
        return df.to_dict(orient="records")

    def wait_for_element(self, by, locator, timeout=20):
        """Waits for an element to be visible and returns it."""
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.visibility_of_element_located((by, locator)))

    def verify_login_page(self, test_data):
        # Open the website
        self.driver.get(self.main_URL)
        # Find the username, password fields, and login button
        username = self.driver.find_element(By.ID, "user-name")
        password = self.driver.find_element(By.ID, "password")

        # Input the username and password
        print(f"\nEntering username and password for {test_data['username']}.")
        username.send_keys(test_data['username'])
        password.send_keys(test_data['password'])

        login_button = self.wait_for_element(By.ID, "login-button")
        print(f"Click on Login button.")
        login_button.click()

    def verify_inventory_page_details(self):
        # Make sure user is logged in and on the inventory page
        self.driver.get(self.main_URL + "/inventory.html")

        # Wait for the inventory list to be visible
        wait = WebDriverWait(self.driver, 10)
        inventory_list = wait.until(
            EC.visibility_of_element_located((By.CLASS_NAME, "inventory_list"))
        )

        # Assert that the inventory page is displayed
        assert inventory_list.is_displayed(), "Inventory page is not displayed"

        # Find all inventory items
        inventory_items = self.driver.find_elements(By.CLASS_NAME, "inventory_item")

        # Assert that there are inventory items
        no_of_inventory_items = len(inventory_items)
        assert no_of_inventory_items > 0, "No items found in the inventory"

        # Loop through each inventory item to extract its details
        print(f"Inventory page has {no_of_inventory_items} items!")
        print("Inventory page items are:")
        # Loop through each inventory item to extract its details
        items_details = []
        for item in inventory_items:
            item_name = item.find_element(By.CLASS_NAME, "inventory_item_name").text
            item_description = item.find_element(By.CLASS_NAME, "inventory_item_desc").text
            item_price = item.find_element(By.CLASS_NAME, "inventory_item_price").text
            # Print out the details of all inventory items
            print(f"{item_name}:{item_price}")
            # Collect all the details in a dictionary
            item_detail = {
                "name": item_name,
                "description": item_description,
                "price": item_price
            }
            items_details.append(item_detail)
        # Store the details in the class-level variable for later use (e.g., cart verification)
        self.driver.inventory_items_details = items_details
        print("Inventory page test has passed!")
        print("------------------------------------------------------")

    def verify_add_item_to_cart(self):
        # Make sure user is on the inventory page
        self.driver.get(self.main_URL + "/inventory.html")
        # Loop through the inventory items to find the backpack
        inventory_items = self.driver.find_elements(By.CLASS_NAME, "inventory_item")
        for item in inventory_items:
            item_name = item.find_element(By.CLASS_NAME, "inventory_item_name").text
            if self.item_wants_to_add in item_name:  # Check if the item contains 'backpack' in the name
                # item_backpack_button = item.wait.until(EC.visibility_of_element_located((By.XPATH, ".//button[contains(@class, 'btn_inventory')]")))
                item_backpack_button = self.wait_for_element(By.XPATH, ".//button[contains(@class, 'btn_inventory')]")
                print(f"\nClicking on the 'Add to Cart' button for: {item_name}")
                item_backpack_button.click()
        cart_count = self.wait_for_element(By.CLASS_NAME, "shopping_cart_badge")
        # Assert that the cart now has 1 item
        print(f"Verifying cart has 1 item in the cart.")
        assert cart_count.text == "1", "Cart count is incorrect"
        print(f"Cart is displaying {cart_count.text} item in the cart.")
        print("Add to cart test has passed!")
        print("------------------------------------------------------")

    # Test for going to the cart page and verifying the item is added
    def verify_cart_page(self):
        try:
            # Go to the cart page
            self.driver.get(self.main_URL + "/cart.html")
            # Wait for the cart item to be visible
            cart_item = self.wait_for_element(By.CLASS_NAME, "cart_item")
            # Assert that the cart page is displayed and has the item
            assert cart_item.is_displayed(), "No items in the cart"
            # Extract item name and price from the cart page
            cart_name = self.wait_for_element(By.CLASS_NAME, "inventory_item_name")
            cart_item_name = cart_name.text
            cart_price = self.wait_for_element(By.CLASS_NAME, "inventory_item_price")
            cart_item_price = cart_price.text
            # Find the corresponding item in the inventory details to compare
            for item in self.driver.inventory_items_details:
                if self.item_wants_to_add == item['name']:
                    if item['name'] == cart_item_name:
                        # Check if the price also matches
                        if item['price'] == cart_item_price:
                            message = f"Added item from inventory page:{self.item_wants_to_add} and showing on cart correct item_name :{cart_item_name} with correct price {cart_item_price}."
                            print(message)
                            print(f"Cart page test has passed !")
                            print("------------------------------------------------------")
                            break
                        else:
                            print("------------------------------------------------------")
                            raise AssertionError(f"price mismatch. Cart page shows: {cart_item_name} with price {cart_item_price} \nand original {item['name']} with price {item['price']}.")
        except Exception as exc:
            print(f"Error in Cart Page: {exc}")
            raise exc

    # Test for reset app state functionality
    def perform_reset_app_state(self):
        try:
            self.driver.get(self.main_URL + "/inventory.html")
            menu_button = self.wait_for_element(By.ID, "react-burger-menu-btn")
            print("Click the menu button to open the user menu.")
            menu_button.click()
            # Wait for the reset_app_state button to be visible
            reset_app_state_button = self.wait_for_element(By.ID, "reset_sidebar_link")
            print(f"Click the reset_app_state button.")
            reset_app_state_button.click()
            print("Finding shopping cart to verify items in it..")
            try:
                cart_count = self.wait_for_element(By.CLASS_NAME, "shopping_cart_badge", timeout=3)
                if cart_count.is_displayed():
                    print("Cart still has items. Reset did not work correctly.")
                    assert False, "Reset_app_state has not worked correctly and the cart still shows items in it."
            except (TimeoutException, NoSuchElementException):
                print("Cart is empty. Reset_app_state has worked correctly.")

        except Exception as exc:
            raise exc

    # Test for logout functionality
    def verify_logout(self):
        self.perform_reset_app_state()
        self.driver.get(self.main_URL + "/inventory.html")
        menu_button =self.wait_for_element(By.ID, "react-burger-menu-btn")
        # Click the menu button to open the user menu
        menu_button.click()
        # Wait for the logout button to be visible
        logout_button = self.wait_for_element(By.ID, "logout_sidebar_link")
        # Click the logout button
        logout_button.click()
        # Assert that we are redirected to the login page
        self.wait_for_element(By.ID, "login-button")
        # Check if the login button is visible to confirm successful logout
        login_button = self.driver.find_element(By.ID, "login-button")
        assert login_button.is_displayed(), "Logout failed, Login button not visible"
        print("Logout test passed and user redirected to the login page!")
        print("------------------------------------------------------")

    def verify_proceed_to_checkout_step_1(self, filling_form_data):
        """Verify valid credentials added to the form and proceed to checkout."""
        self.driver.get(self.main_URL + "/checkout-step-one.html")
        # Fill the form with parameters
        first_name = filling_form_data['First_Name']
        last_name = filling_form_data['Last_Name']
        zip_code = filling_form_data['Postal_code']
        print(f"Verifying with first_name, last_name, zip_code and proceed to checkout.")
        self.driver.find_element(By.ID, "first-name").send_keys(first_name)
        self.driver.find_element(By.ID, "last-name").send_keys(last_name)
        self.driver.find_element(By.ID, "postal-code").send_keys(zip_code)
        if filling_form_data['Credential '] == "Valid":
            continue_button = self.wait_for_element(By.ID, "continue")
            continue_button.click()

    def verify_proceed_to_checkout_continue_button(self, test_data, filling_form_data):
        try:
            self.verify_proceed_to_checkout_step_1(filling_form_data)
            if test_data['username'] != "problem_user":
                self.verify_checkout_overview(test_data)
                self.verify_checkout_complete(test_data)
            else:
                error_message = self.driver.find_element(By.CSS_SELECTOR, ".error-message-container")
                assert error_message.is_displayed(), "Error message not displayed"
                message =f"\nContinue button from proceed to checkout for {test_data['username']} failed due to {error_message.text}!, hence we can not do any further process. "
                print(message)
                self.perform_reset_app_state()
                print("------------------------------------------------------")
        except Exception as exc:
            raise exc

    def verify_checkout_overview(self, test_data):
        """checkout overview process display added item info"""
        print(f"Continue button from proceed to checkout for {test_data['username']} passed!")
        print("------------------------------------------------------")
        print("Verify checkout overview process display added item info.")
        self.driver.get(self.main_URL + "/checkout-step-two.html")
        summary_info = self.wait_for_element(By.CLASS_NAME, "summary_info")
        # Assert that the cart page is displayed and has the item
        assert summary_info.is_displayed(), "No items in the cart"
        summary_info_text = summary_info.text
        last_index = summary_info_text.find("Cancel")  # Find the last of the relevant info
        if last_index != -1:
            clean_summary = summary_info_text[:last_index]  # Extract the relevant info
            clean_summary_info= clean_summary.strip()
            print(f"checkout overview process test has passed and displaying added item info:\n{clean_summary_info} !")
            print("------------------------------------------------------")

    def verify_checkout_complete(self, test_data):
        """checkout complete process display order dispatched info."""
        print("Verify checkout complete process display order dispatched info.")
        try:
            if test_data['username'] != "error_user":
                finish_button = WebDriverWait(self.driver, 20).until(
                    EC.element_to_be_clickable((By.ID, "finish"))
                )
                finish_button.click()
                checkout_info = self.wait_for_element(By.CLASS_NAME, "checkout_complete_container")
                # Assert that the cart page is displayed and has the item
                assert checkout_info.is_displayed(), "No items in the cart"
                checkout_info_text = checkout_info.text
                last_index = checkout_info_text.find("Back Home")  # Find the last of the relevant info
                if last_index != -1:
                    clean_summary = checkout_info_text[:last_index]  # Extract the relevant info
                    clean_summary_info = clean_summary.strip()
                    print(
                        f"Checkout complete process test passed and displaying order dispatched info as below:\n{clean_summary_info}")
                    back_home_button = self.driver.find_element(By.ID, "back-to-products")
                    back_home_button.click()
                    print("------------------------------------------------------")
            else:
                self.perform_reset_app_state()
                raise AssertionError("Checkout should not proceed for error_user.")
        except Exception as exc:
            print("Finish button is not clickable. " + str(exc))
            raise exc

# Execute the tests programmatically
if __name__ == "__main__":
    test_sauce = TestSauce()
    test_sauce.run_tests()
