"""
test_saucedemo_2_page.py file runs automatically using run_tests.py file.
"""
import pytest
import os

def run_tests(test_dir=None, test_file="test_saucedemo_2_page.py", base_url=None):
    # Default test directory
    if test_dir is None:
        test_dir = os.getcwd()  # Get the current working directory by default

    # Construct the full path for the test file or directory
    test_path = os.path.join(test_dir, test_file)

    # Check if the test file exists
    if not os.path.isfile(test_path):
        print(f"Error: Test file '{test_path}' does not exist.")
        return

    # Prepare pytest arguments
    pytest_args = ["-v", "-s", test_path]

    if base_url:
        pytest_args.append(f"--base-url={base_url}")

    # Run pytest
    pytest.main(pytest_args)

if __name__ == "__main__":
    # Get base URL from environment variable (optional)
    base_url = os.getenv("BASE_URL")

    # Run tests with optional base URL
    run_tests()



