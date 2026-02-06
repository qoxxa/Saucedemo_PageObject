import re

import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait

from DataProvider import DataProvider

class CartPage:
    def __init__(self, driver: WebDriver) ->None:
        self.url = DataProvider().get("urls.base")
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        self.data = DataProvider().get

    @allure.step("Открыть корзину")
    def open_cart(self):
        icon_cart = self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, self.data("selectors.cart_page.cart_icon"))))
        icon_cart.click()

    @allure.step("Проверка заголовка страницы - корзина")
    def page_cart_title(self):
        title = self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, self.data("selectors.cart_page.cart_title"))))
        return title.text

    @allure.step("Получить список цен")
    def get_prices(self):
        prices = self.wait.until(
            EC.visibility_of_all_elements_located((By.CSS_SELECTOR, self.data("selectors.product_page.prices"))))
        return [e.text for e in prices]

    @allure.step("Получить названия товаров")
    def get_product_names(self):
        names = self.wait.until(
            EC.visibility_of_all_elements_located((By.CSS_SELECTOR, self.data("selectors.product_page.product_names"))))
        return [e.text for e in names]

    @allure.step("Убрать товар из корзины")
    def remove_from_cart(self, product_key: str):
        product_id = DataProvider().get(f"product_ids.{product_key}")
        template = DataProvider().get("selectors.product_page.remove_btn_template")

        selector = template.format(product_id)
        btn_remove = self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, selector)))
        btn_remove.click()

    @allure.step("Клик по кнопке - проверка")
    def checkout_click(self):
        btn_checkout = self.wait.until(
            EC.element_to_be_clickable((By.ID, self.data("selectors.cart_page.checkout_btn"))))
        btn_checkout.click()

    @allure.step("Проверка заголовка страницы оформления")
    def title_checkout(self):
        title = self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, self.data("selectors.cart_page.title_checkout"))))
        return title.text
