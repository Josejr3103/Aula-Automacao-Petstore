import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService


def get_driver(browser: str = "chrome", headless: bool = True):
    browser = browser.lower()

    if browser == "chrome":
        options = webdriver.ChromeOptions()
        if headless:
            options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--window-size=1920,1080")

        driver_path = os.environ.get("CHROMEDRIVER_PATH")
        service = ChromeService(executable_path=driver_path) if driver_path else ChromeService()
        return webdriver.Chrome(service=service, options=options)

    if browser == "firefox":
        options = webdriver.FirefoxOptions()
        if headless:
            options.add_argument("--headless")

        driver_path = os.environ.get("GECKODRIVER_PATH")
        service = FirefoxService(executable_path=driver_path) if driver_path else FirefoxService()
        return webdriver.Firefox(service=service, options=options)

    raise ValueError(f"Unsupported browser: '{browser}'. Use 'chrome' or 'firefox'.")