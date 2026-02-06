import re

import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait

from DataProvider import DataProvider


class ProductPage:
    def __init__(self, driver: WebDriver) ->None:
        self.url = DataProvider().get("urls.base")
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        self.data = DataProvider().get

    @allure.step("Перейти на карточку товара")
    def go_product(self):
        product = self.wait.until(
            EC.visibility_of_element_located((By.XPATH, self.data("selectors.product_page.product_backpack"))))
        product.click()

    @allure.step("Проверить наименование товара")
    def check_product_name(self):
        product_name = self.wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, self.data("selectors.product_page.product_name"))))
        return product_name.text

    @allure.step("Проверить цену товара")
    def check_product_price(self):
        product_price = self.wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, self.data("selectors.product_page.product_price"))))
        return product_price.text

    @allure.step("Добавить товары в корзину")
    def add_to_cart(self, product_key: str):
        # Получаем значение из selectors.product_page.id_XXX
        product_id = DataProvider().get(f"product_ids.{product_key}")
        template = DataProvider().get("selectors.product_page.add_to_cart_template")

        selector = template.format(product_id)
        button = self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, selector)))
        button.click()

    @allure.step("Убрать товар из корзины")
    def remove_from_cart(self, product_key: str):
        product_id = DataProvider().get(f"product_ids.{product_key}")
        template = DataProvider().get("selectors.product_page.remove_btn_template")

        selector = template.format(product_id)
        btn_remove = self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, selector)))
        btn_remove.click()

    @allure.step("Отображение товаров в иконке корзины")
    def check_icon_cart(self):
        icon = self.wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, self.data("selectors.product_page.icon_cart"))))
        return icon.text

    @allure.step("Сортировка")
    def sort_container(self, sort_by):
        btn_sort = self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, self.data("selectors.product_page.sort_container"))))
        select = Select(btn_sort)
        select.select_by_value(sort_by)

    @allure.step("Получить список цен")
    def get_prices(self):
        prices = self.wait.until(
            EC.visibility_of_all_elements_located((By.CSS_SELECTOR, self.data("selectors.product_page.prices"))))
        return [e.text for e in prices]

    @allure.step("Проверка активной кнопки сортировки")
    def get_active_sort_option(self):
        option = self.wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, self.data("selectors.product_page.active_sort_option"))))
        return option.text

    @allure.step("Получить названия товаров")
    def get_product_names(self):
        names = self.wait.until(
            EC.visibility_of_all_elements_located((By.CSS_SELECTOR, self.data("selectors.product_page.product_names"))))
        return [e.text for e in names]

    @allure.step("Очистить цену от доп.знаков")
    def extract_price(self, price_str: str) -> float:
        return float(re.sub(r'[^\d.]', '', price_str))