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
        WebDriverWait(self.driver, 10).until(
            EC.url_contains("checkout-step-one.html")
        )
        # Captura o texto atual para debug
        texto_atual = self.get_text(self._PAGE_TITLE)
        print(f"\nDEBUG: Texto capturado na página de Checkout: '{texto_atual}'")
    
        # Validação com tratamento de espaços
        return "Checkout: Your Information" in texto_atual.strip()

    def fill_customer_info(self, first_name: str, last_name: str, postal_code: str):
        self.type(self._FIRST_NAME, first_name)
        self.type(self._LAST_NAME, last_name)
        self.type(self._POSTAL_CODE, postal_code)

    def continue_to_overview(self):
        # ✅ Força clique via JS (consistência com CI/headless)
        btn = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self._CONTINUE_BUTTON)
        )
        self.driver.execute_script("arguments[0].click();", btn)

        # ✅ Aguarda a navegação completar antes de retornar
        WebDriverWait(self.driver, 10).until(
            EC.url_contains("checkout-step-two.html")
        )


class CheckoutStepTwoPage(BasePage):
    _PAGE_TITLE = (By.CLASS_NAME, "title")
    _FINISH_BUTTON = (By.ID, "finish")
    _SUMMARY_TOTAL = (By.CLASS_NAME, "summary_total_label")

    def is_on_checkout_overview(self) -> bool:
        # ✅ Garante que a página carregou antes de ler o título
        WebDriverWait(self.driver, 10).until(
            EC.url_contains("checkout-step-two.html")
        )
        return self.get_text(self._PAGE_TITLE) == "Checkout: Overview"

    def get_total(self) -> str:
        return self.get_text(self._SUMMARY_TOTAL)

    def finish_order(self):
        btn = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self._FINISH_BUTTON)
        )
        self.driver.execute_script("arguments[0].click();", btn)

        WebDriverWait(self.driver, 10).until(
            EC.url_contains("checkout-complete.html")
        )

class CheckoutCompletePage(BasePage):
    _COMPLETE_HEADER = (By.CLASS_NAME, "complete-header")

    def get_confirmation_message(self) -> str:
        return self.get_text(self._COMPLETE_HEADER)
