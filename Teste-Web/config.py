# config.py — Configurações centrais do projeto Selenium

BASE_URL = "https://www.saucedemo.com"

USERS = {
    "standard": {
        "username": "standard_user",
        "password": "secret_sauce",
    },
    "locked": {
        "username": "locked_out_user",
        "password": "secret_sauce",
    },
}

CHECKOUT_INFO = {
    "first_name": "João",
    "last_name":  "Silva",
    "postal_code": "12345-678",
}

BROWSER_OPTIONS = {
    "headless":           False,
    "implicit_wait":      10,
    "page_load_timeout":  30,
}
