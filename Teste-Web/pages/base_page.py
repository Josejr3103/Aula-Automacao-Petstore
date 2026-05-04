# selenium/pages/base_page.py

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from typing import List


class BasePage:
    """Classe base com ações genéricas reutilizáveis por todos os Page Objects."""

    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.wait   = WebDriverWait(driver, timeout=10)

    # ── Navegação ──────────────────────────────────────────────────────────────

    def open(self, url: str) -> None:
        self.driver.get(url)

    @property
    def current_url(self) -> str:
        return self.driver.current_url

    # ── Localização ───────────────────────────────────────────────────────────

    def find(self, by: str, value: str) -> WebElement:
        return self.wait.until(EC.visibility_of_element_located((by, value)))

    def find_clickable(self, by: str, value: str) -> WebElement:
        return self.wait.until(EC.element_to_be_clickable((by, value)))

    def find_all(self, by: str, value: str) -> List[WebElement]:
        return self.wait.until(EC.presence_of_all_elements_located((by, value)))

    # ── Interações ────────────────────────────────────────────────────────────

    def click(self, by: str, value: str) -> None:
        self.find_clickable(by, value).click()

    def type_text(self, by: str, value: str, text: str) -> None:
        el = self.find(by, value)
        el.clear()
        el.send_keys(text)

    def get_text(self, by: str, value: str) -> str:
        return self.find(by, value).text

    # ── Verificações ──────────────────────────────────────────────────────────

    def is_visible(self, by: str, value: str) -> bool:
        try:
            return self.find(by, value).is_displayed()
        except Exception:
            return False

    def url_contains(self, fragment: str) -> bool:
        return fragment in self.driver.current_url
