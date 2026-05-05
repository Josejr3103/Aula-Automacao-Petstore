from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage


class CartPage(BasePage):
    _PAGE_TITLE = (By.CLASS_NAME, "title")
    _CART_ITEMS = (By.CLASS_NAME, "cart_item")
    _CHECKOUT_BUTTON = (By.ID, "checkout")

    def is_on_cart_page(self) -> bool:
        self.wait.until(EC.presence_of_element_located(self._CHECKOUT_BUTTON))
        return True

    def get_item_count(self) -> int:
        self.wait.until(EC.presence_of_element_located(self._CART_ITEMS))
        return len(self.driver.find_elements(*self._CART_ITEMS))

    def proceed_to_checkout(self):
        self.click(self._CHECKOUT_BUTTON)
