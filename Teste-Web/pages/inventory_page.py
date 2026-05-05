from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage


class InventoryPage(BasePage):
    _PAGE_TITLE = (By.CLASS_NAME, "title")
    _ADD_TO_CART_BUTTONS = (By.CSS_SELECTOR, "[data-test^='add-to-cart']")
    _CART_BADGE = (By.CLASS_NAME, "shopping_cart_badge")
    _CART_LINK = (By.CLASS_NAME, "shopping_cart_link")

    def is_on_inventory_page(self) -> bool:
        return self.get_text(self._PAGE_TITLE) == "Products"

    def add_products_to_cart(self, count: int = 2):
        for _ in range(count):
            buttons = self.wait.until(
                EC.presence_of_all_elements_located(self._ADD_TO_CART_BUTTONS)
            )
            buttons[0].click()

    def get_cart_item_count(self) -> int:
        return int(self.get_text(self._CART_BADGE))

    def go_to_cart(self):
        self.click(self._CART_LINK)
