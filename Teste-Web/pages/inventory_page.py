from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


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
    
    def wait_for_cart_count(self, expected_count):
        if expected_count > 0:
            try:
                WebDriverWait(self.driver, 5).until(
                    EC.visibility_of_element_located(self._CART_BADGE)
                )
                WebDriverWait(self.driver, 5).until(
                    EC.text_to_be_present_in_element(self._CART_BADGE, str(expected_count))
                )
            except Exception as e:
                raise e
        else:
            WebDriverWait(self.driver, 5).until(
                EC.invisibility_of_element_located(self._CART_BADGE)
            )

    def get_cart_item_count(self) -> int:
        return int(self.get_text(self._CART_BADGE))

    def go_to_cart(self):
        cart_icon = self.driver.find_element(By.CLASS_NAME, "shopping_cart_link")
        self.driver.execute_script("arguments[0].click();", cart_icon)
