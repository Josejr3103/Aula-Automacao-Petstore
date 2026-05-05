from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class CheckoutStepOnePage(BasePage):
    _PAGE_TITLE = (By.CLASS_NAME, "title")
    _FIRST_NAME = (By.ID, "first-name")
    _LAST_NAME = (By.ID, "last-name")
    _POSTAL_CODE = (By.ID, "postal-code")
    _CONTINUE_BUTTON = (By.ID, "continue")

    def is_on_checkout_step_one(self) -> bool:
        # 1. Aguarda até 10 segundos para garantir que a página carregou
        # Substitua 'self._PAGE_TITLE' pelo locator do seu elemento (ex: By.CLASS_NAME, 'title')
        try:
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(self._PAGE_TITLE)
            )
            # 2. Agora que o elemento está visível, extrai o texto e compara
            texto_atual = self.get_text(self._PAGE_TITLE).strip()
            return "Checkout: Your Information" in texto_atual
        except Exception as e:
            print(f"DEBUG: Falha ao carregar a página de checkout: {e}")
            return False

    def fill_customer_info(self, first_name: str, last_name: str, postal_code: str):
        self.type(self._FIRST_NAME, first_name)
        self.type(self._LAST_NAME, last_name)
        self.type(self._POSTAL_CODE, postal_code)

    def continue_to_overview(self):
        self.click(self._CONTINUE_BUTTON)


class CheckoutStepTwoPage(BasePage):
    _PAGE_TITLE = (By.CLASS_NAME, "title")
    _FINISH_BUTTON = (By.ID, "finish")
    _SUMMARY_TOTAL = (By.CLASS_NAME, "summary_total_label")

    def is_on_checkout_overview(self) -> bool:
        return self.get_text(self._PAGE_TITLE) == "Checkout: Overview"

    def get_total(self) -> str:
        return self.get_text(self._SUMMARY_TOTAL)

    def finish_order(self):
        self.click(self._FINISH_BUTTON)


class CheckoutCompletePage(BasePage):
    _COMPLETE_HEADER = (By.CLASS_NAME, "complete-header")

    def get_confirmation_message(self) -> str:
        return self.get_text(self._COMPLETE_HEADER)
