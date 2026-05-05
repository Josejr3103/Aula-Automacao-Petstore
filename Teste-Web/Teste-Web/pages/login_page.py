from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class LoginPage(BasePage):
    URL = "https://www.saucedemo.com/"

    _USERNAME = (By.ID, "user-name")
    _PASSWORD = (By.ID, "password")
    _LOGIN_BUTTON = (By.ID, "login-button")
    _ERROR_MESSAGE = (By.CSS_SELECTOR, "[data-test='error']")

    def open(self):
        self.driver.get(self.URL)

    def login(self, username: str, password: str):
        self.type(self._USERNAME, username)
        self.type(self._PASSWORD, password)
        self.click(self._LOGIN_BUTTON)

    def get_error_message(self) -> str:
        return self.get_text(self._ERROR_MESSAGE)
