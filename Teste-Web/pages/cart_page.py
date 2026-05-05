from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage


class CartPage(BasePage):
    _PAGE_TITLE = (By.CLASS_NAME, "title")
    _CART_ITEMS = (By.CLASS_NAME, "cart_item")
    _CHECKOUT_BUTTON = (By.ID, "checkout")

    def is_on_cart_page(self) -> bool:
        try:
            # Aumente para 20 ou 30 segundos para teste inicial
            self.wait.until(lambda d: d.execute_script("return document.readyState") == "complete")
            self.wait.until(EC.element_to_be_clickable(self._CHECKOUT_BUTTON))
            return True
        except Exception as e:
            print(f"DEBUG: URL atual é {self.driver.current_url}")
            print(f"DEBUG: Título da página é {self.driver.title}")
            # Tira print para ver o que está na tela no momento da falha
            self.driver.save_screenshot("erro_checkout.png")
            raise e # Relança o erro para o pytest continuar marcando como falha

    def get_item_count(self) -> int:
        self.wait.until(EC.presence_of_element_located(self._CART_ITEMS))
        return len(self.driver.find_elements(*self._CART_ITEMS))

    def proceed_to_checkout(self):
        self.click(self._CHECKOUT_BUTTON)
