from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from selenium.webdriver.support import expected_conditions as EC


class CartPage(BasePage):
    _PAGE_TITLE = (By.CLASS_NAME, "title")
    _CART_ITEMS = (By.CLASS_NAME, "cart_item")
    _CHECKOUT_BUTTON = (By.ID, "checkout")

    def is_on_cart_page(self) -> bool:
        texto_capturado = self.get_text(self._PAGE_TITLE)
        print(f"\nDEBUG: Texto capturado no título: '{texto_capturado}'")
        return texto_capturado == "Your Cart"

    def get_item_count(self) -> int:
        return len(self.driver.find_elements(*self._CART_ITEMS))

    def proceed_to_checkout(self):
        self.click(self._CHECKOUT_BUTTON)
