"""
This file(utility file) is used for all activities/functionalities related to webpages handling using selenium web driver.
"""
#sauce_lib.py
import os
import time
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
            driver = webdriver.Edge()
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

    def wait_for_element(self, by, locator, timeout=20):
        """Waits for an element to be visible and returns it."""
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.visibility_of_element_located((by, locator)))

    def verify_login_page(self, test_data):
        # Open the website
        try:
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
        except Exception as exc:
            raise exc

    def verify_inventory_page_details(self):
        # Make sure user is logged in and on the inventory page
        try:
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
            self.capture_screenshot("")

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
        except Exception as exc:
            # Perform logout
            print("Logging out due to failure...")
            self.verify_logout()
            raise exc

    def verify_add_item_to_cart(self):
        try:
            # Make sure user is on the inventory page
            self.driver.get(self.main_URL + "/inventory.html")
            # Loop through the inventory items to find the backpack
            inventory_items = self.driver.find_elements(By.CLASS_NAME, "inventory_item")
            for item in inventory_items:
                item_name = item.find_element(By.CLASS_NAME, "inventory_item_name").text
                if self.item_wants_to_add in item_name:  # Check if the item contains 'backpack' in the name
                    # item_backpack_button = item.wait.until(EC.visibility_of_element_located((By.XPATH, ".//button[contains(@class, 'btn_inventory')]")))
                    item_backpack_button = self.wait_for_element(By.XPATH,
                                                                 ".//button[contains(@class, 'btn_inventory')]")
                    print(f"\nClicking on the 'Add to Cart' button for: {item_name}")
                    item_backpack_button.click()
                    self.capture_screenshot("")
            cart_count = self.wait_for_element(By.CLASS_NAME, "shopping_cart_badge")
            # Assert that the cart now has 1 item
            print(f"Verifying cart has 1 item in the cart.")
            assert cart_count.text == "1", "Cart count is incorrect"
            self.capture_screenshot("")
            print(f"Cart is displaying {cart_count.text} item in the cart.")
            print("Add to cart test has passed!")
            print("------------------------------------------------------")
        except Exception as exc:
            # Perform logout
            print("Logging out due to failure...")
            self.verify_logout()
            raise exc

    def verify_cart_page(self):
        try:
            # Go to the cart page
            self.driver.get(self.main_URL + "/cart.html")
            # Wait for the cart item to be visible
            cart_item = self.wait_for_element(By.CLASS_NAME, "cart_item")
            assert cart_item.is_displayed(), "No items in the cart"

            # Extract item name and price from the cart page
            cart_name = self.wait_for_element(By.CLASS_NAME, "inventory_item_name")
            cart_item_name = cart_name.text
            cart_price = self.wait_for_element(By.CLASS_NAME, "inventory_item_price")
            cart_item_price = cart_price.text

            # Debug prints
            print(f"Cart item name: {cart_item_name}, Cart price: {cart_item_price}")
            print(f"Checking inventory details...")

            # Find the corresponding item in the inventory details
            for item in self.driver.inventory_items_details:
                if self.item_wants_to_add == item['name']:
                    expected_price = item['price'].replace("$", "").strip()
                    actual_price = cart_item_price.replace("$", "").strip()

                    print(f"DEBUG: Expected item: {item['name']}, Expected price: {expected_price}")

                    if item['name'] == cart_item_name and expected_price == actual_price:
                        print(f"Cart page test passed! Correct item '{cart_item_name}' with price {cart_item_price}.")
                        print("------------------------------------------------------")
                        break
                    else:
                        print("------------------------------------------------------")
                        self.capture_screenshot("")
                        raise AssertionError(
                            f"Price mismatch: Cart shows {cart_item_name} with price {cart_item_price}, "
                            f"expected {item['name']} with price {item['price']}.")
        except Exception as exc:
            print(f"Error in Cart Page: {exc}")
            # Perform logout
            print("Logging out due to failure...")
            self.verify_logout()
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
        try:
            self.perform_reset_app_state()
            self.driver.get(self.main_URL + "/inventory.html")
            menu_button = self.wait_for_element(By.ID, "react-burger-menu-btn")
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
        except Exception as exc:
            raise exc

    def verify_proceed_to_checkout_continue_button(self, test_data):
        """Verify valid credentials added to the form and proceed to checkout."""
        try:
            self.driver.get(self.main_URL + "/checkout-step-one.html")

            first_name = test_data.get('First_Name', "")
            last_name = test_data.get('Last_Name', "")
            zip_code = test_data.get('Postal_code', "")

            print(
                f"Filling checkout form: First Name = '{first_name}', Last Name = '{last_name}', Zip Code = '{zip_code}'")

            # Fill in the first name and postal code fields
            self.driver.find_element(By.ID, "first-name").send_keys(first_name)
            self.driver.find_element(By.ID, "postal-code").send_keys(zip_code)

            # Check if the last name field is editable before filling it
            last_name_field = self.wait_for_element(By.ID, "last-name")
            if last_name_field.is_enabled():
                last_name_field.send_keys(last_name)
                # Ensure the continue button is clickable
                continue_button = self.wait_for_element(By.ID, "continue")
                if continue_button.is_enabled():
                    print("Clicking the Continue button.")
                    continue_button.click()
                    if test_data['username'] == "problem_user":
                        error_message = self.wait_for_element(By.CSS_SELECTOR, ".error-message-container")
                        if error_message.is_displayed():
                            self.capture_screenshot("last_name_error")
                            message = f"\nContinue button from proceed to checkout for {test_data['username']} failed due to {error_message.text}!, hence we can not do any further process. "
                            print(message)
                            raise AssertionError("Checkout failed because the Continue button is not clickable.")
                    else:
                        print(f"Continue button from proceed to checkout for {test_data['username']} passed!")
                        print("------------------------------------------------------")
                        self.verify_checkout_overview()
                        self.verify_checkout_complete()

        except Exception as exc:
            print("Logging out due to failure...")
            self.verify_logout()
            raise exc


    def verify_checkout_overview(self):
        """checkout overview process display added item info"""
        try:
            print("Verify checkout overview process display added item info.")
            # self.driver.get(self.main_URL + "/checkout-step-two.html")
            summary_info = self.wait_for_element(By.CLASS_NAME, "summary_info")
            # Assert that the cart page is displayed and has the item
            assert summary_info.is_displayed(), "No items in the cart"
            self.capture_screenshot("")
            time.sleep(10)
            summary_info_text = summary_info.text
            last_index = summary_info_text.find("Cancel")  # Find the last of the relevant info
            if last_index != -1:
                clean_summary = summary_info_text[:last_index]  # Extract the relevant info
                clean_summary_info = clean_summary.strip()
                print(
                    f"checkout overview process test has passed and displaying added item info:\n{clean_summary_info} !")
                print("------------------------------------------------------")
        except Exception as exc:
            raise exc

    def verify_checkout_complete(self):
        """Verify checkout complete process and display order dispatched info."""
        print("Verify checkout complete process display order dispatched info.")

        try:
            # Debug: Print the current page URL
            print(f"Current page URL: {self.driver.current_url}")

            # Wait for the "Finish" button to be clickable
            try:
                finish_button = WebDriverWait(self.driver, 20).until(
                    EC.element_to_be_clickable((By.ID, "finish"))
                )
                assert finish_button.is_displayed(), "Finish button is not visible!"
                assert finish_button.is_enabled(), "Finish button is disabled!"

                print("Finish button is visible and enabled. Clicking now...")
                finish_button.click()
            except (TimeoutException, NoSuchElementException) as exc:
                raise AssertionError(
                    "Finish button was not clickable! Checkout cannot proceed.") from exc

            # Wait for the checkout complete container
            try:
                checkout_info = self.wait_for_element(By.CLASS_NAME, "checkout_complete_container")
                assert checkout_info.is_displayed(), "Checkout info container is not displayed!"
                self.capture_screenshot("")
            except (TimeoutException, NoSuchElementException) as exc:
                raise AssertionError("Checkout complete container did not appear after clicking Finish!") from exc

            # Extract checkout information
            checkout_info_text = checkout_info.text
            last_index = checkout_info_text.find("Back Home")
            clean_summary_info = checkout_info_text[
                                 :last_index].strip() if last_index != -1 else checkout_info_text.strip()

            print(f"Checkout complete! Order dispatched info:\n{clean_summary_info}")

            # Click "Back Home" button
            try:
                back_home_button = self.driver.find_element(By.ID, "back-to-products")
                back_home_button.click()
                print("Checkout process completed successfully and navigated back to products page.")
                print("Checkout process test has passed.")
                print("------------------------------------------------------")
            except (TimeoutException, NoSuchElementException) as exc:
                raise AssertionError(" 'Back Home' button was not found or not clickable!") from exc

        except Exception as exc:
            print(f"Error in checkout process: {exc}")
            raise exc  # Reraise the original exception

    def capture_screenshot(self, filename):
        """Capture a screenshot and save it to the 'screenshots' directory."""
        try:
            screenshots_dir = os.path.join(os.getcwd(), "screenshots")
            if not os.path.exists(screenshots_dir):
                os.makedirs(screenshots_dir)  # Create the directory if it doesn’t exist

            timestamp = time.strftime("%Y%m%d-%H%M%S")
            filepath = os.path.join(screenshots_dir, f"{filename}_{timestamp}.png")
            self.driver.save_screenshot(filepath)

            print(f"Screenshot saved: {filepath}")
        except Exception as e:
            print(f"Failed to capture screenshot: {e}")


# Execute the tests programmatically
if __name__ == "__main__":
    test_sauce = TestSauce()
    test_sauce.run_tests()
    test_sauce.capture_screenshot("test")
