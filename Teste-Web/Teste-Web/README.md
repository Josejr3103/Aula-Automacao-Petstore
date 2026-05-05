# Teste-Web — Automação E2E SauceDemo

Projeto de testes automatizados end-to-end utilizando **Selenium + pytest** com arquitetura **Page Object Model (POM)**.

## Estrutura

```
Teste-Web/
├── pages/
│   ├── base_page.py          # Ações genéricas do Selenium
│   ├── login_page.py
│   ├── inventory_page.py
│   ├── cart_page.py
│   └── checkout_page.py
├── tests/
│   └── test_purchase_flow.py # Teste E2E completo
├── utils/
│   └── driver_factory.py     # Inicialização do WebDriver
├── conftest.py               # Fixtures do pytest
├── pytest.ini
└── requirements.txt
```

## Instalação

```bash
pip install -r requirements.txt
```

## Execução

```bash
# Padrão: Chrome headless
pytest

# Com browser visível
pytest --headless=false

# Usando Firefox
pytest --browser=firefox
```

## Fluxo testado

1. Abre `https://www.saucedemo.com/`
2. Realiza login com `standard_user`
3. Adiciona 2 produtos ao carrinho
4. Acessa o carrinho e valida os itens
5. Preenche informações de checkout
6. Confirma o pedido e valida a mensagem de conclusão
