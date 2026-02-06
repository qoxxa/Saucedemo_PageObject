from time import sleep

import allure

from DataProvider import DataProvider
from conftest import product_page
@allure.title("Открыть корзину")
@allure.description("Открыть пустую корзину товаров")
@allure.id(1)
@allure.severity("Critical")
def test_open_cart(cart_page):
    actual_url = DataProvider().get("urls.cart")
    actual_title = DataProvider().get("page_titles.cart")

    cart_page.open_cart()
    title = cart_page.page_cart_title()

    assert actual_title == title
    assert cart_page.driver.current_url == actual_url

@allure.title("Добавить товар в корзину")
@allure.description("Проверка корректности добавления товара")
@allure.id(2)
@allure.severity("Critical")
def test_add_to_cart(cart_page, product_page):
    backpack_name = DataProvider().get("products.backpack.name")

    product_page.add_to_cart("backpack")
    cart_page.open_cart()

    product_name = cart_page.get_product_names()

    assert len(product_name) == 1
    assert cart_page.get_product_names() == [backpack_name]

@allure.title("Добавить товары в корзину")
@allure.description("Проверка корректности добавления нескольких товаров")
@allure.id(3)
@allure.severity("Critical")
def test_add_multiple_items_to_cart(cart_page, product_page):
    backpack = DataProvider().get("products.backpack")
    light= DataProvider().get("products.light")

    product_page.add_to_cart("backpack")
    product_page.add_to_cart("bike_light")

    cart_page.open_cart()

    product_names = cart_page.get_product_names()
    product_prices = cart_page.get_prices()

    expected_names = {backpack["name"], light["name"]}
    expected_prices = {backpack["price"], light["price"]}

    assert len(product_names) == 2
    assert len(product_prices) == 2
    assert set(product_names) == expected_names
    assert set(product_prices) == expected_prices

@allure.title("Удалить товар из корзины")
@allure.description("Удаление товара на странице - корзина")
@allure.id(4)
@allure.severity("Critical")
def test_remove_from_cart(cart_page,product_page):
    product_page.add_to_cart("backpack")
    product_page.add_to_cart("bike_light")

    cart_page.open_cart()
    cart_page.remove_from_cart("backpack")

    product_names = cart_page.get_product_names()

    assert len(product_names) == 1

@allure.title("Переход на страницу оформления заказа")
@allure.description("Проверка работы кнопки перехода")
@allure.id(5)
@allure.severity("Critical")
def test_checkout(cart_page, product_page):
    actual_title = DataProvider().get("page_titles.checkout")
    actual_url = DataProvider().get("urls.checkout")

    product_page.add_to_cart("backpack")

    cart_page.open_cart()
    cart_page.checkout_click()
    title = cart_page.title_checkout()

    assert actual_title == title
    assert actual_url == cart_page.driver.current_url

