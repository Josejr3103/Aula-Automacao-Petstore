# selenium/pages/inventory_page.py

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from pages.base_page import BasePage
from typing import List


class InventoryPage(BasePage):
    """Page Object da listagem de produtos."""

    _TITLE         = (By.CLASS_NAME, "title")
    _PRODUCT_NAMES = (By.CLASS_NAME, "inventory_item_name")
    _PRODUCT_PRICES= (By.CLASS_NAME, "inventory_item_price")
    _SORT_DROPDOWN = (By.CLASS_NAME, "product_sort_container")
    _CART_ICON     = (By.CLASS_NAME, "shopping_cart_link")
    _CART_BADGE    = (By.CLASS_NAME, "shopping_cart_badge")

    def _add_btn(self, product_name: str) -> tuple:
        slug = (product_name.lower()
                .replace(" ", "-")
                .replace("(", "")
                .replace(")", ""))
        return (By.ID, f"add-to-cart-{slug}")

    def _remove_btn(self, product_name: str) -> tuple:
        slug = (product_name.lower()
                .replace(" ", "-")
                .replace("(", "")
                .replace(")", ""))
        return (By.ID, f"remove-{slug}")

    # ── Ações ─────────────────────────────────────────────────────────────────

    def add_product(self, product_name: str) -> "InventoryPage":
        self.click(*self._add_btn(product_name))
        return self

    def remove_product(self, product_name: str) -> "InventoryPage":
        self.click(*self._remove_btn(product_name))
        return self

    def sort_products(self, option: str) -> "InventoryPage":
        """option: 'az' | 'za' | 'lohi' | 'hilo'"""
        Select(self.find(*self._SORT_DROPDOWN)).select_by_value(option)
        return self

    def go_to_cart(self) -> None:
        self.click(*self._CART_ICON)

    # ── Verificações ─────────────────────────────────────────────────────────

    def get_product_names(self) -> List[str]:
        return [el.text for el in self.find_all(*self._PRODUCT_NAMES)]

    def get_cart_count(self) -> int:
        if self.is_visible(*self._CART_BADGE):
            return int(self.get_text(*self._CART_BADGE))
        return 0

    def is_on_inventory_page(self) -> bool:
        return self.url_contains("inventory")
