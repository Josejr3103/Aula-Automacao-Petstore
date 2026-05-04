# selenium/pages/checkout_page.py

from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from typing import List


class CheckoutStepOnePage(BasePage):
    """Step 1 do checkout: dados pessoais."""

    _FIRST_NAME   = (By.ID, "first-name")
    _LAST_NAME    = (By.ID, "last-name")
    _POSTAL_CODE  = (By.ID, "postal-code")
    _BTN_CONTINUE = (By.ID, "continue")
    _BTN_CANCEL   = (By.ID, "cancel")
    _ERROR        = (By.CSS_SELECTOR, "[data-test='error']")

    def fill_info(self, first: str, last: str, zip_code: str) -> "CheckoutStepOnePage":
        self.type_text(*self._FIRST_NAME, first)
        self.type_text(*self._LAST_NAME, last)
        self.type_text(*self._POSTAL_CODE, zip_code)
        return self

    def click_continue(self) -> None:
        self.click(*self._BTN_CONTINUE)

    def click_cancel(self) -> None:
        self.click(*self._BTN_CANCEL)

    def has_error(self) -> bool:
        return self.is_visible(*self._ERROR)

    def get_error(self) -> str:
        return self.get_text(*self._ERROR)

    def is_on_step_one(self) -> bool:
        return self.url_contains("checkout-step-one")


class CheckoutStepTwoPage(BasePage):
    """Step 2 do checkout: resumo do pedido."""

    _ITEM_NAMES  = (By.CLASS_NAME, "inventory_item_name")
    _TOTAL_LABEL = (By.CLASS_NAME, "summary_total_label")
    _BTN_FINISH  = (By.ID, "finish")
    _BTN_CANCEL  = (By.ID, "cancel")

    def get_order_items(self) -> List[str]:
        return [el.text for el in self.find_all(*self._ITEM_NAMES)]

    def get_total(self) -> str:
        return self.get_text(*self._TOTAL_LABEL)

    def click_finish(self) -> None:
        self.click(*self._BTN_FINISH)

    def click_cancel(self) -> None:
        self.click(*self._BTN_CANCEL)

    def is_on_step_two(self) -> bool:
        return self.url_contains("checkout-step-two")


class CheckoutCompletePage(BasePage):
    """Tela de confirmação do pedido."""

    _HEADER      = (By.CLASS_NAME, "complete-header")
    _TEXT        = (By.CLASS_NAME, "complete-text")
    _BTN_BACK    = (By.ID, "back-to-products")

    def get_header(self) -> str:
        return self.get_text(*self._HEADER)

    def get_body_text(self) -> str:
        return self.get_text(*self._TEXT)

    def go_back_to_products(self) -> None:
        self.click(*self._BTN_BACK)

    def is_confirmed(self) -> bool:
        return self.is_visible(*self._HEADER)

    def is_on_complete_page(self) -> bool:
        return self.url_contains("checkout-complete")
