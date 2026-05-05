import pytest
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import (
    CheckoutStepOnePage,
    CheckoutStepTwoPage,
    CheckoutCompletePage,
)
from selenium.webdriver.support import expected_conditions as EC

VALID_USERNAME = "standard_user"
VALID_PASSWORD = "secret_sauce"
PRODUCTS_TO_ADD = 2


class TestPurchaseFlow:
    @pytest.fixture(autouse=True)
    def setup(self, driver, wait):
        """
        Injeta o driver e o wait configurados no conftest.py
        """
        self.driver = driver
        self.wait = wait  # Agora o 'wait' está disponível na classe
        
        self.login_page = LoginPage(driver)
        self.inventory_page = InventoryPage(driver)
        self.cart_page = CartPage(driver)
        self.checkout_step_one = CheckoutStepOnePage(driver)
        self.checkout_step_two = CheckoutStepTwoPage(driver)
        self.checkout_complete = CheckoutCompletePage(driver)

    def test_e2e_purchase(self):
        self.login_page.open()
        self.login_page.login(VALID_USERNAME, VALID_PASSWORD)
        
        # Sincronização explícita com as transições de página
        self.wait.until(EC.url_contains("inventory.html"))
        assert self.inventory_page.is_on_inventory_page()

        self.inventory_page.add_products_to_cart(PRODUCTS_TO_ADD)
        assert self.inventory_page.get_cart_item_count() == PRODUCTS_TO_ADD

        self.inventory_page.go_to_cart()
        self.wait.until(EC.url_contains("cart.html"))
        assert self.cart_page.is_on_cart_page()
        assert self.cart_page.get_item_count() == PRODUCTS_TO_ADD

        self.cart_page.proceed_to_checkout()
        self.wait.until(EC.url_contains("checkout-step-one.html"))
        assert self.checkout_step_one.is_on_checkout_step_one()

        self.checkout_step_one.fill_customer_info("João", "Silva", "50000-000")
        self.checkout_step_one.continue_to_overview()
        
        self.wait.until(EC.url_contains("checkout-step-two.html"))
        assert self.checkout_step_two.is_on_checkout_overview()
        
        self.checkout_step_two.finish_order()
        
        self.wait.until(EC.url_contains("checkout-complete.html"))
        confirmation = self.checkout_complete.get_confirmation_message()
        assert confirmation == "Thank you for your order!"