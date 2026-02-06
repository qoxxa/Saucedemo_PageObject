import re
import allure

from DataProvider import DataProvider
from conftest import product_page

@allure.title("Открыть карточку")
@allure.description("Открыть карточку товара - рюкзак")
@allure.id(1)
@allure.severity("Critical")
def test_open_card_product(product_page):
    product = DataProvider().get("products.backpack")

    product_page.go_product()
    actual_name = product_page.check_product_name()
    actual_price = product_page.check_product_price()

    assert actual_name == product["name"]
    assert actual_price == product["price"]

@allure.title("Добавить товары в корзину")
@allure.description("Проверить кол-во товаров отображаемое иконкой")
@allure.id(2)
@allure.severity("Critical")
def test_add_to_cart(product_page):
    product_page.add_to_cart("backpack")
    product_page.add_to_cart("bike_light")
    quantity = product_page.check_icon_cart()

    assert quantity == "2"

@allure.title("Убрать товар из корзины")
@allure.description("Удалить товар через кнопку под фото товара")
@allure.id(4)
@allure.severity("Medium")
def test_delete_from_card(product_page):
    product_page.add_to_cart("backpack")
    product_page.add_to_cart("bike_light")
    product_page.remove_from_cart("backpack")
    quantity = product_page.check_icon_cart()

    assert quantity == "1"

@allure.title("Сортировка по возрастанию")
@allure.description("Сортировка по возрастанию")
@allure.id(4)
@allure.severity("Medium")
def test_sort_asc(product_page):
    sort_value = DataProvider().get("sort_options.asc")

    product_page.sort_container(sort_value)
    prices = product_page.get_prices()
    numeric_prices = [float(re.sub(r'[^\d.]', '', p)) for p in prices]

    assert numeric_prices == sorted(numeric_prices)

@allure.title("Сортировка убыванию")
@allure.description("Сортировка по убыванию")
@allure.id(5)
@allure.severity("Medium")
def test_sort_desc(product_page):
    sort_value = DataProvider().get("sort_options.desc")

    product_page.sort_container(sort_value)
    prices = product_page.get_prices()
    numeric_prices = [float(re.sub(r'[^\d.]', '', p)) for p in prices]

    assert numeric_prices == sorted(numeric_prices, reverse=True)
    print (numeric_prices)

@allure.title("Сортировка по алфавиту (A-Z)")
@allure.description("Сортировка по наименованию товара")
@allure.id(6)
@allure.severity("Medium")
def test_sort_desc(product_page):
    sort_value = DataProvider().get("sort_options.a-z")

    product_page.sort_container(sort_value)
    names = product_page.get_product_names()

    assert names == sorted(names)

@allure.title("Сортировка по алфавиту (Z-A)")
@allure.description("Сортировка по наименованию товара")
@allure.id(7)
@allure.severity("Medium")
def test_sort_desc(product_page):
    sort_value = DataProvider().get("sort_options.z-a")

    product_page.sort_container(sort_value)
    names = product_page.get_product_names()

    assert names == sorted(names, reverse=True)