# selenium/pages/burger_menu_page.py

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage


class BurgerMenuPage(BasePage):
    """
    Page Object do menu lateral (hamburguer) do SauceDemo.

    O botão de abertura tem id='react-burger-menu-btn'.
    O menu expõe quatro opções:
      - All Items       → volta ao inventário
      - About           → abre site da Sauce Labs
      - Logout          → encerra sessão
      - Reset App State → limpa carrinho e estado da aplicação
    """

    # ── Locators ─────────────────────────────────────────────────────────────
    _BTN_OPEN  = (By.ID, "react-burger-menu-btn")
    _BTN_CLOSE = (By.ID, "react-burger-cross-btn")

    _LINK_ALL_ITEMS    = (By.ID, "inventory_sidebar_link")
    _LINK_ABOUT        = (By.ID, "about_sidebar_link")
    _LINK_LOGOUT       = (By.ID, "logout_sidebar_link")
    _LINK_RESET        = (By.ID, "reset_sidebar_link")

    _MENU_CONTAINER    = (By.CLASS_NAME, "bm-menu-wrap")

    # ── Ações ─────────────────────────────────────────────────────────────────

    def open_menu(self) -> "BurgerMenuPage":
        """Clica no botão hamburguer e aguarda o menu aparecer."""
        self.click(*self._BTN_OPEN)
        # Aguarda o menu ficar visível (aria-hidden muda para false)
        self.wait.until(
            EC.visibility_of_element_located(self._LINK_LOGOUT)
        )
        return self

    def close_menu(self) -> "BurgerMenuPage":
        """Fecha o menu pelo botão X interno."""
        self.click(*self._BTN_CLOSE)
        # Aguarda o menu sair da tela
        self.wait.until(
            EC.invisibility_of_element_located(self._LINK_LOGOUT)
        )
        return self

    def click_all_items(self) -> None:
        """Navega para a listagem de produtos."""
        self.click(*self._LINK_ALL_ITEMS)

    def click_about(self) -> None:
        """Abre a página institucional da Sauce Labs."""
        self.click(*self._LINK_ABOUT)

    def click_logout(self) -> None:
        """Desloga e retorna à tela de login."""
        self.click(*self._LINK_LOGOUT)

    def click_reset_app_state(self) -> None:
        """
        Reseta o estado da aplicação:
        - Esvazia o carrinho
        - Remove o estado de botões 'Remove' (voltam a 'Add to cart')
        """
        self.click(*self._LINK_RESET)

    # ── Verificações ─────────────────────────────────────────────────────────

    def is_menu_open(self) -> bool:
        """Retorna True se o menu lateral estiver visível."""
        return self.is_visible(*self._LINK_LOGOUT)

    def is_menu_closed(self) -> bool:
        return not self.is_menu_open()
