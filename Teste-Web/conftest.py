# selenium/conftest.py

import pytest
from utils.driver_factory import DriverFactory
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.burger_menu_page import BurgerMenuPage
from pages.checkout_page import (
    CheckoutStepOnePage,
    CheckoutStepTwoPage,
    CheckoutCompletePage,
)
from config import USERS


def pytest_addoption(parser):
    parser.addoption(
        "--browser",
        action="store",
        default="chrome",
        help="chrome (padrão) ou firefox",
    )


@pytest.fixture(scope="function")
def driver(request):
    """Cria e destrói o WebDriver a cada teste — isolamento garantido."""
    browser = request.config.getoption("--browser")
    drv = DriverFactory.get_driver(browser)
    yield drv
    drv.quit()


@pytest.fixture(scope="function")
def logged_in(driver):
    """
    Fixture que realiza o login com o usuário padrão e devolve
    um dict com o driver e todos os Page Objects prontos.
    """
    login = LoginPage(driver)
    login.open_login_page()
    login.login(
        USERS["standard"]["username"],
        USERS["standard"]["password"],
    )
    return {
        "driver":     driver,
        "inventory":  InventoryPage(driver),
        "cart":       CartPage(driver),
        "burger":     BurgerMenuPage(driver),
        "checkout1":  CheckoutStepOnePage(driver),
        "checkout2":  CheckoutStepTwoPage(driver),
        "complete":   CheckoutCompletePage(driver),
    }
