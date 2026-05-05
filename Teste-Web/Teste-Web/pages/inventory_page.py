from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class InventoryPage(BasePage):
    _PAGE_TITLE = (By.CLASS_NAME, "title")
    _PRODUCT_ITEMS = (By.CLASS_NAME, "inventory_item")
    _ADD_TO_CART_BUTTONS = (By.CSS_SELECTOR, "[data-test^='add-to-cart']")
    _CART_BADGE = (By.CLASS_NAME, "shopping_cart_badge")
    _CART_LINK = (By.CLASS_NAME, "shopping_cart_link")

    def is_on_inventory_page(self) -> bool:
        return self.get_text(self._PAGE_TITLE) == "Products"

    def add_products_to_cart(self, count: int = 2):
        buttons = self.driver.find_elements(*self._ADD_TO_CART_BUTTONS)
        for button in buttons[:count]:
            button.click()

    def get_cart_item_count(self) -> int:
        return int(self.get_text(self._CART_BADGE))

    def go_to_cart(self):
        self.click(self._CART_LINK)
