import os
import pytest
import allure
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium import webdriver
from DataProvider import DataProvider
from tests.MainPage import MainPage


@pytest.fixture(scope='session')
def browser():
    headless = os.getenv("HEADLESS", "false").lower() == "true"
    timeout = 10
    browser_name = DataProvider().get('browser_name').lower()
    prefs = {"profile.password_manager_leak_detection": False}

    if browser_name == 'chrome':
        options = ChromeOptions()
        if headless:
            options.add_argument("--headless")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--disable-password-manager")
        options.add_argument("--disable-save-password-bubble")
        options.add_argument("--disable-infobars")
        options.add_argument("--disable-extensions")
        options.add_experimental_option("prefs", prefs)
        browser = webdriver.Chrome(options=options)

    elif browser_name == 'firefox':
        options = FirefoxOptions()
        if headless:
            options.add_argument("--headless")
        options.add_argument("--width=1920")
        options.add_argument("--height=1080")
        browser = webdriver.Firefox(options=options)

    else:
        raise ValueError(f"Неподдерживаемый браузер: {browser_name}. Поддерживаются: 'chrome', 'firefox'.")

    browser.implicitly_wait(timeout)
    yield browser

    with allure.step("Закрыть браузер"):
        browser.quit()

@pytest.fixture()
def main_page(browser):
    main_page = MainPage(browser)
    main_page.go()
    return main_page




