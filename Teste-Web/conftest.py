import pytest
from utils.driver_factory import get_driver


def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome")
    parser.addoption("--headless", action="store", default="False")


@pytest.fixture(scope="session")
def browser(request):
    return request.config.getoption("--browser")


@pytest.fixture(scope="session")
def headless(request):
    return request.config.getoption("--headless").lower() == "true"


@pytest.fixture()
def driver(browser, headless):
    driver = get_driver(browser=browser, headless=headless)
    yield driver
    driver.quit()
