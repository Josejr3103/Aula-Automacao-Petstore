# selenium/tests/test_e2e_purchase.py
#
# Fluxo E2E completo do SauceDemo
# ─────────────────────────────────────────────────────────────────────────────
# Etapas cobertas:
#   1. Login com usuário válido
#   2. Menu hamburguer (abrir / fechar / Reset App State / Logout / All Items)
#   3. Adição de múltiplos produtos ao carrinho
#   4. Verificação do carrinho
#   5. Checkout Step 1 — preenchimento de dados
#   6. Checkout Step 2 — revisão e confirmação do pedido
#   7. Tela de confirmação e retorno ao inventário
# ─────────────────────────────────────────────────────────────────────────────

import pytest
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.burger_menu_page import BurgerMenuPage
from pages.checkout_page import (
    CheckoutStepOnePage,
    CheckoutStepTwoPage,
    CheckoutCompletePage,
)
from config import USERS, CHECKOUT_INFO

# Produtos utilizados ao longo de toda a suite
PRODUCTS = [
    "Sauce Labs Backpack",
    "Sauce Labs Bike Light",
    "Sauce Labs Bolt T-Shirt",
]


class TestE2EFullPurchaseFlow:
    """
    Suite E2E que cobre o fluxo completo de compra,
    incluindo todas as funcionalidades do menu hamburguer.
    """

    # ══════════════════════════════════════════════════════════════════════════
    # CT-01 — Login
    # ══════════════════════════════════════════════════════════════════════════

    def test_01_login_com_usuario_valido(self, driver):
        """
        Verifica que o usuário padrão consegue autenticar
        e é redirecionado para a página de inventário.
        """
        login = LoginPage(driver)
        login.open_login_page()
        login.login(
            USERS["standard"]["username"],
            USERS["standard"]["password"],
        )

        inventory = InventoryPage(driver)
        assert inventory.is_on_inventory_page(), (
            "Após login válido deve redirecionar para /inventory"
        )

    # ══════════════════════════════════════════════════════════════════════════
    # CT-02 a CT-06 — Menu Hamburguer
    # ══════════════════════════════════════════════════════════════════════════

    def test_02_menu_hamburger_abre_e_fecha(self, logged_in):
        """
        CT-02: Clicar no botão id='react-burger-menu-btn' abre o menu lateral.
        Clicar no X interno fecha o menu.
        """
        burger = logged_in["burger"]

        # --- Abre ---
        burger.open_menu()
        assert burger.is_menu_open(), (
            "Menu deve estar visível após clicar em react-burger-menu-btn"
        )

        # --- Fecha ---
        burger.close_menu()
        assert burger.is_menu_closed(), (
            "Menu deve estar oculto após clicar no botão de fechar"
        )

    def test_03_menu_all_items_retorna_ao_inventario(self, logged_in):
        """
        CT-03: Opção 'All Items' do menu deve navegar (ou permanecer)
        na listagem de produtos.
        """
        burger    = logged_in["burger"]
        inventory = logged_in["inventory"]

        burger.open_menu()
        burger.click_all_items()

        assert inventory.is_on_inventory_page(), (
            "'All Items' deve direcionar para /inventory"
        )

    def test_04_menu_reset_app_state_esvazia_carrinho(self, logged_in):
        """
        CT-04: 'Reset App State' deve limpar o carrinho e resetar
        o estado dos botões 'Add to cart' / 'Remove'.

        Fluxo:
          1. Adiciona produto → carrinho mostra badge = 1
          2. Abre menu → clica Reset
          3. Badge desaparece → carrinho está vazio
        """
        inventory = logged_in["inventory"]
        burger    = logged_in["burger"]

        # Adiciona um produto
        inventory.add_product(PRODUCTS[0])
        assert inventory.get_cart_count() == 1, "Badge deve mostrar 1"

        # Reseta via menu
        burger.open_menu()
        burger.click_reset_app_state()

        # Badge deve desaparecer (count = 0)
        assert inventory.get_cart_count() == 0, (
            "Reset App State deve esvaziar o carrinho (badge = 0)"
        )

    def test_05_menu_logout_encerra_sessao(self, logged_in):
        """
        CT-05: 'Logout' deve encerrar a sessão e redirecionar para
        a tela de login.
        """
        burger = logged_in["burger"]
        login  = LoginPage(logged_in["driver"])

        burger.open_menu()
        burger.click_logout()

        assert login.url_contains("saucedemo.com"), (
            "Após logout deve retornar à tela de login"
        )
        assert not login.url_contains("inventory"), (
            "Usuário não deve ter acesso ao inventário após logout"
        )

    def test_06_nao_acessa_inventario_apos_logout(self, logged_in):
        """
        CT-06: Após logout, tentar acessar /inventory diretamente
        deve redirecionar de volta para a tela de login (proteção de rota).
        """
        burger = logged_in["burger"]
        driver = logged_in["driver"]

        burger.open_menu()
        burger.click_logout()

        # Tenta acessar rota protegida manualmente
        driver.get("https://www.saucedemo.com/inventory.html")

        login = LoginPage(driver)
        assert not login.url_contains("inventory"), (
            "Rota protegida deve redirecionar para login após sessão encerrada"
        )

    # ══════════════════════════════════════════════════════════════════════════
    # CT-07 a CT-09 — Produtos e Carrinho
    # ══════════════════════════════════════════════════════════════════════════

    def test_07_adicionar_multiplos_produtos(self, logged_in):
        """
        CT-07: Adicionar 3 produtos ao carrinho.
        Badge deve acumular corretamente.
        """
        inventory = logged_in["inventory"]

        for product in PRODUCTS:
            inventory.add_product(product)

        assert inventory.get_cart_count() == len(PRODUCTS), (
            f"Badge deve marcar {len(PRODUCTS)} após adicionar todos os produtos"
        )

    def test_08_produtos_aparecem_no_carrinho(self, logged_in):
        """
        CT-08: Os produtos adicionados devem constar na tela do carrinho.
        """
        inventory = logged_in["inventory"]
        cart      = logged_in["cart"]

        for product in PRODUCTS:
            inventory.add_product(product)

        inventory.go_to_cart()

        assert cart.is_on_cart_page(), "Deve estar na página do carrinho"
        for product in PRODUCTS:
            assert cart.is_product_in_cart(product), (
                f"'{product}' deve constar no carrinho"
            )

    def test_09_reset_apos_adicionar_varios_produtos(self, logged_in):
        """
        CT-09: Reset App State limpa o carrinho mesmo com vários itens.
        Confirma que o estado da UI (badge) é zerado.
        """
        inventory = logged_in["inventory"]
        burger    = logged_in["burger"]

        for product in PRODUCTS:
            inventory.add_product(product)

        assert inventory.get_cart_count() == len(PRODUCTS)

        burger.open_menu()
        burger.click_reset_app_state()

        assert inventory.get_cart_count() == 0, (
            "Reset deve zerar o badge independente da quantidade de itens"
        )

    # ══════════════════════════════════════════════════════════════════════════
    # CT-10 — Fluxo E2E Completo (happy path)
    # ══════════════════════════════════════════════════════════════════════════

    def test_10_fluxo_completo_de_compra(self, logged_in):
        """
        CT-10 (HAPPY PATH): Fluxo ponta a ponta completo.

        Login → Verificar menu → Adicionar produtos →
        Carrinho → Checkout Step 1 → Step 2 → Confirmação →
        Retornar ao inventário via menu 'All Items'

        ┌─────────────┐   ┌───────────┐   ┌───────────┐
        │   Inventory │──▶│   Cart    │──▶│ Checkout  │
        │  (+ burger) │   │           │   │ Step 1    │
        └─────────────┘   └───────────┘   └─────┬─────┘
                                                 │
                                          ┌──────▼──────┐
                                          │  Step 2     │
                                          │  (resumo)   │
                                          └──────┬──────┘
                                                 │
                                          ┌──────▼──────┐
                                          │ Confirmação │
                                          │ + All Items │
                                          └─────────────┘
        """
        inventory  = logged_in["inventory"]
        burger     = logged_in["burger"]
        cart       = logged_in["cart"]
        checkout1  = logged_in["checkout1"]
        checkout2  = logged_in["checkout2"]
        complete   = logged_in["complete"]

        # ── ETAPA 1: Verificar menu hamburguer antes de comprar ───────────────
        burger.open_menu()
        assert burger.is_menu_open(), "Menu deve abrir ao clicar no hamburguer"
        burger.close_menu()
        assert burger.is_menu_closed(), "Menu deve fechar corretamente"

        # ── ETAPA 2: Adicionar produtos ao carrinho ───────────────────────────
        for product in PRODUCTS:
            inventory.add_product(product)

        assert inventory.get_cart_count() == len(PRODUCTS), (
            "Badge deve refletir a quantidade correta de produtos"
        )

        # ── ETAPA 3: Ir ao carrinho e verificar itens ─────────────────────────
        inventory.go_to_cart()
        assert cart.is_on_cart_page()
        assert cart.item_count() == len(PRODUCTS), (
            "Carrinho deve ter a mesma quantidade de itens adicionados"
        )
        for product in PRODUCTS:
            assert cart.is_product_in_cart(product), (
                f"'{product}' deve estar no carrinho"
            )

        # ── ETAPA 4: Checkout Step 1 — dados pessoais ─────────────────────────
        cart.proceed_to_checkout()
        assert checkout1.is_on_step_one(), "Deve estar no checkout step 1"

        checkout1.fill_info(
            CHECKOUT_INFO["first_name"],
            CHECKOUT_INFO["last_name"],
            CHECKOUT_INFO["postal_code"],
        )
        checkout1.click_continue()

        # ── ETAPA 5: Checkout Step 2 — resumo do pedido ───────────────────────
        assert checkout2.is_on_step_two(), "Deve estar no checkout step 2"

        order_items = checkout2.get_order_items()
        for product in PRODUCTS:
            assert product in order_items, (
                f"'{product}' deve constar no resumo do pedido"
            )

        total = checkout2.get_total()
        assert total, "Total do pedido deve ser exibido"

        checkout2.click_finish()

        # ── ETAPA 6: Confirmação ──────────────────────────────────────────────
        assert complete.is_on_complete_page(), "Deve estar na página de confirmação"
        assert complete.is_confirmed(), "Mensagem de confirmação deve estar visível"
        assert "thank you" in complete.get_header().lower(), (
            "Header de confirmação deve conter 'Thank you'"
        )

        # ── ETAPA 7: Voltar ao inventário via botão Back Home ─────────────────
        complete.go_back_to_products()
        assert inventory.is_on_inventory_page(), (
            "Botão 'Back Home' deve redirecionar para o inventário"
        )

        # ── ETAPA 8: Confirma que o carrinho está zerado após compra ──────────
        assert inventory.get_cart_count() == 0, (
            "Carrinho deve estar vazio após finalizar a compra"
        )

    # ══════════════════════════════════════════════════════════════════════════
    # CT-11 — Validação de formulário no Checkout
    # ══════════════════════════════════════════════════════════════════════════

    def test_11_checkout_sem_dados_exibe_erro(self, logged_in):
        """
        CT-11: Avançar no Step 1 sem preencher dados deve exibir erro
        e manter o usuário na mesma página.
        """
        inventory = logged_in["inventory"]
        cart      = logged_in["cart"]
        checkout1 = logged_in["checkout1"]

        inventory.add_product(PRODUCTS[0])
        inventory.go_to_cart()
        cart.proceed_to_checkout()

        checkout1.click_continue()  # sem preencher nada

        assert checkout1.has_error(), "Deve exibir mensagem de erro"
        assert checkout1.is_on_step_one(), "Deve permanecer no Step 1"

    # ══════════════════════════════════════════════════════════════════════════
    # CT-12 — About (smoke: só verifica que o link existe e é clicável)
    # ══════════════════════════════════════════════════════════════════════════

    def test_12_menu_about_link_acessivel(self, logged_in):
        """
        CT-12: O link 'About' deve estar presente e clicável no menu.
        (Verifica existência sem navegar para fora do domínio de testes)
        """
        burger = logged_in["burger"]
        driver = logged_in["driver"]

        burger.open_menu()

        # Verifica que o link está presente antes de clicar
        from selenium.webdriver.common.by import By
        about_link = driver.find_element(By.ID, "about_sidebar_link")
        assert about_link.is_displayed(), "Link 'About' deve estar visível no menu"
        assert about_link.get_attribute("href") is not None, (
            "Link 'About' deve possuir um href válido"
        )

        burger.close_menu()
