# selenium/pages/login_page.py

from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from config import BASE_URL


class LoginPage(BasePage):
    """Page Object da tela de Login."""

    _USERNAME = (By.ID, "user-name")
    _PASSWORD = (By.ID, "password")
    _BTN_LOGIN = (By.ID, "login-button")
    _ERROR     = (By.CSS_SELECTOR, "[data-test='error']")

    def open_login_page(self) -> "LoginPage":
        self.open(BASE_URL)
        return self

    def login(self, username: str, password: str) -> None:
        self.type_text(*self._USERNAME, username)
        self.type_text(*self._PASSWORD, password)
        self.click(*self._BTN_LOGIN)

    def get_error_message(self) -> str:
        return self.get_text(*self._ERROR)

    def has_error(self) -> bool:
        return self.is_visible(*self._ERROR)
