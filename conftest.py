import os
import pytest
import allure
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium import webdriver
from DataProvider import DataProvider
from pages.login_page import LoginPage
from pages.product_page import ProductPage
from pages.card_page import CartPage

@pytest.fixture(scope='session')
def browser():
    headless = os.getenv("HEADLESS", "false").lower() == "true"
    timeout = 10
    browser_name = DataProvider().get("browsers.chrome").lower()
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

def _login_and_navigate(browser, url_key, page_class):
    user = DataProvider().get("users.standard")
    url = DataProvider().get(url_key)

    # Логинимся
    login_page = LoginPage(browser)
    login_page.go()
    login_page.do_login(user["login"], user["password"])

    # Очищаем состояние (только после загрузки домена!)
    browser.execute_script("window.localStorage.clear();")
    browser.execute_script("window.sessionStorage.clear();")

    # Переходим на целевую страницу
    browser.get(url)

    return page_class(browser)

@pytest.fixture()
def login_page(browser):
    login_page = LoginPage(browser)
    login_page.go()
    return login_page

@pytest.fixture()
def product_page(browser):
    return _login_and_navigate(browser, "urls.products", ProductPage)

@pytest.fixture()
def cart_page(browser):
    return _login_and_navigate(browser, "urls.cart", CartPage)


