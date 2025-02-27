# swag_labs
Task: Enter into website:https://www.saucedemo.com/ and do front-end E2E test.

Solution:
I have tested manually and automated this website:https://www.saucedemo.com/ and created testcases, executed in "Test Rail" and automated them using below scripts.
I have created different files where different purposes serve as below to perform above task:

1. test_saucedemo_2_page.py : This script(driver file) will enter into website:https://www.saucedemo.com/ and do front-end E2E tests using Selenium framework.
2. sauce_lib.py:  This file(utility file) is used for all activities/functionalities related to webpages handling using selenium web driver. 
3. run_tests.py: test_saucedemo_2_page.py file runs automatically using run_tests.py file.
4. test_data.xlsx: This file provide test data where all users and their information has stored.
5. conftest.py: This file is responsible for configuring pytest for different environment.

There are two main below test scenarios conducted using pytest and test data(which is stored in "test_data.xlsx") from the fixture where all users information added.

1. Test Login page functionality.
2. Test End-to-End Process functionality which is all page test activities shown step by step as below.
   
STEP 1: Test for login functionality.

STEP 2: Test for inventory page after successful login.

STEP 3: Test for add an item to the cart page.

STEP 4: Test for cart page after adding item to cart.

STEP 5: Test for checkout process.

STEP 6: Test for Logout process.

During tests generated screenshots stored in cretaed new folder screenshots.

To Run this solution please follow below steps:

1. Install the dependencies by running: pip install -r requirements.txt
2. Run run_tests.py 
You will successfully execute this above code.

GitHub workflows to run the front-end tests Monday to Friday at noon has also set up.

Currently three major bugs in the website and that's why three testcases are failing.

1.Problem User: Continue button from proceed to checkout for problem_user failed due to Error: Last Name is required!, hence we can not do any further process.

2.Error User: Error in checkout process: Checkout complete container did not appear after clicking Finish!

3.Visual User: Error in Cart Page: Price mismatch.

I have tested and executed all users against end to end process through manually and automated testing as above and generated test result bug stored in "swag_labs_bug_all_users.xlsx"

For more detail test runs and result, you can find in my Test Rail account, where I have mentioned all comments and attached screenshots as well.
