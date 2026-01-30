import allure
from DataProvider import DataProvider
from conftest import main_page


@allure.title("Авторизация")
@allure.description("Авторизация через стандартный логин")
@allure.id(1)
@allure.severity("Blocked")
def test_standart_login(main_page):
    login = DataProvider().get("standart")
    password = DataProvider().get("password")

    main_page.login_authorization(login, password)
    check_transition = main_page.checking_products()

    assert main_page.driver.current_url == "https://www.saucedemo.com/inventory.html"
    assert check_transition == "Products"


@allure.title("Неверный пароль")
@allure.description("Авторизация с неверным паролем")
@allure.id(2)
@allure.severity("Critical")
def test_invalid_password(main_page):
    login = DataProvider().get("standart")
    password = "invalid_password"

    main_page.login_authorization(login, password)
    check_error = main_page.checking_error()

    assert main_page.driver.current_url == "https://www.saucedemo.com/"
    assert check_error == "Epic sadface: Username and password do not match any user in this service"

@allure.title("Заблокированный пользователь")
@allure.description("Авторизация заблокированного пользователя")
@allure.id(3)
@allure.severity("Critical")
def test_locked_username(main_page):
    login = DataProvider().get("locked_out")
    password = DataProvider().get("password")

    main_page.login_authorization(login, password)
    check_error = main_page.checking_error()

    assert main_page.driver.current_url == "https://www.saucedemo.com/"
    assert check_error == "Epic sadface: Sorry, this user has been locked out."

@allure.title("Пустые поля ввода")
@allure.description("Авторизация с пустыми полями ввода")
@allure.id(5)
@allure.severity("Critical")
def test_empty_fields(main_page):
    main_page.click_login_button()
    check_error = main_page.checking_error()

    assert main_page.driver.current_url == "https://www.saucedemo.com/"
    assert check_error == "Epic sadface: Username is required"

def test_performance_glitch(main_page):
    login = DataProvider().get("performance_glitch")
    password = DataProvider().get("password")

    main_page.login_authorization(login, password)
    check_transition = main_page.checking_products()

    assert main_page.driver.current_url == "https://www.saucedemo.com/inventory.html"
    assert check_transition == "Products"
