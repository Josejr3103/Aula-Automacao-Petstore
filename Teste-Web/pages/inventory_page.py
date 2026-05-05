from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage


class InventoryPage(BasePage):
    _PAGE_TITLE = (By.CLASS_NAME, "title")
    _ADD_TO_CART_BUTTONS = (By.CSS_SELECTOR, "[data-test^='add-to-cart']")
    _CART_BADGE = (By.CLASS_NAME, "shopping_cart_badge")
    _CART_LINK = (By.CLASS_NAME, "shopping_cart_link")

    def is_on_inventory_page(self) -> bool:
        self.wait.until(EC.url_contains("inventory"))
        return True

    def add_products_to_cart(self, quantity):
        buttons = self.driver.find_elements(*self._ADD_TO_CART_BUTTONS)
        for i in range(quantity):
            buttons[i].click()
            # Em vez de esperar pelo texto, esperamos pela atualização da contagem
            # Aumentamos o tempo caso o CI precise de um pouco mais de fôlego
            self.wait.until(lambda d: d.find_element(*self._CART_BADGE).text == str(i + 1))

    def get_cart_item_count(self) -> int:
        return int(self.get_text(self._CART_BADGE))

    def go_to_cart(self):
        self.driver.find_element(*self._CART_LINK).click()
