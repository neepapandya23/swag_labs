import pytest
import os

def run_tests(test_dir=None, test_file="test_saucedemo_2_page.py"):
    # Default test directory
    if test_dir is None:
        test_dir = os.getcwd()  # Get the current working directory by default

    # Construct the full path for the test file or directory
    test_path = os.path.join(test_dir, test_file)

    # Check if the test file exists
    if not os.path.isfile(test_path):
        print(f"Error: Test file '{test_path}' does not exist.")
        return

    # Run pytest with verbose and print options, and save allure results
    pytest.main(["-v", "-s", test_path])

if __name__ == "__main__":
    # By default, this will run tests in the "tests" folder with the test file "test_saucedemo_2_page.py"
    run_tests()  # Uses default values

