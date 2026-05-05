from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage

class CheckoutStepOnePage(BasePage):
    _PAGE_TITLE = (By.CLASS_NAME, "title")
    _FIRST_NAME = (By.ID, "first-name")
    _LAST_NAME = (By.ID, "last-name")
    _POSTAL_CODE = (By.ID, "postal-code")
    _CONTINUE_BUTTON = (By.ID, "continue")

    def is_on_checkout_step_one(self) -> bool:
        self.wait.until(EC.url_contains("checkout-step-one"))
        return True

    def fill_customer_info(self, first_name: str, last_name: str, postal_code: str):
        self.type(self._FIRST_NAME, first_name)
        self.type(self._LAST_NAME, last_name)
        self.type(self._POSTAL_CODE, postal_code)

    def continue_to_overview(self):
        self.click(self._CONTINUE_BUTTON)


class CheckoutStepTwoPage(BasePage):
    _PAGE_TITLE = (By.CLASS_NAME, "title")
    _FINISH_BUTTON = (By.ID, "finish")
    _SUMMARY_TOTAL = (By.CLASS_NAME, "summary_total_label")

    def is_on_checkout_overview(self) -> bool:
        self.wait.until(EC.url_contains("checkout-step-two"))
        return True

    def get_total(self) -> str:
        return self.get_text(self._SUMMARY_TOTAL)

    def finish_order(self):
        self.click(self._FINISH_BUTTON)


class CheckoutCompletePage(BasePage):
    _COMPLETE_HEADER = (By.CLASS_NAME, "complete-header")

    def get_confirmation_message(self) -> str:
        return self.get_text(self._COMPLETE_HEADER)
