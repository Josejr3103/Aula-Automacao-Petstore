# selenium/pages/cart_page.py

from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from typing import List


class CartPage(BasePage):
    """Page Object do carrinho de compras."""

    _CART_ITEMS  = (By.CLASS_NAME, "cart_item")
    _ITEM_NAMES  = (By.CLASS_NAME, "inventory_item_name")
    _BTN_CHECKOUT       = (By.ID, "checkout")
    _BTN_CONTINUE_SHOP  = (By.ID, "continue-shopping")

    def _remove_btn(self, product_name: str) -> tuple:
        slug = (product_name.lower()
                .replace(" ", "-")
                .replace("(", "")
                .replace(")", ""))
        return (By.ID, f"remove-{slug}")

    # ── Ações ─────────────────────────────────────────────────────────────────

    def remove_item(self, product_name: str) -> "CartPage":
        self.click(*self._remove_btn(product_name))
        return self

    def proceed_to_checkout(self) -> None:
        self.click(*self._BTN_CHECKOUT)

    def continue_shopping(self) -> None:
        self.click(*self._BTN_CONTINUE_SHOP)

    # ── Verificações ─────────────────────────────────────────────────────────

    def get_product_names(self) -> List[str]:
        return [el.text for el in self.find_all(*self._ITEM_NAMES)]

    def item_count(self) -> int:
        return len(self.find_all(*self._CART_ITEMS))

    def is_product_in_cart(self, name: str) -> bool:
        return name in self.get_product_names()

    def is_empty(self) -> bool:
        return self.item_count() == 0

    def is_on_cart_page(self) -> bool:
        return self.url_contains("cart")
