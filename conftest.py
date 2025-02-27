"""
This file is responsible for configuring pytest for different environment.
"""
import pytest
import os

def pytest_addoption(parser):
    """Adds a command-line option for base URL"""
    parser.addoption(
        "--base-url",
        action="store",
        default=os.getenv("BASE_URL", "https://www.saucedemo.com"),
        help="Base URL for the test environment"
    )

@pytest.fixture
def base_url(request):
    """Fixture to get base URL from command-line or environment variable"""
    return request.config.getoption("--base-url")

