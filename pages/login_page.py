import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from DataProvider import DataProvider


class LoginPage:
    def __init__(self, driver: WebDriver) ->None:
        self.url = DataProvider().get("urls.base")
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        self.data = DataProvider().get

    @allure.step("Перейти на сайт")
    def go(self):
        self.driver.get(self.url)

    @allure.step("Аутентификация пользователя")
    def do_login(self, username, password):
        self.go()
        self.login(username)
        self.password(password)
        self.login_button()

    @allure.step("Ввод логина")
    def login(self, standard):
        login_field = self.wait.until(EC.visibility_of_element_located((By.ID, self.data("selectors.login_page.username"))))
        login_field.send_keys(standard)

    @allure.step("Ввод пароля")
    def password(self, password):
        password_field = self.wait.until(EC.visibility_of_element_located((By.ID, self.data("selectors.login_page.password"))))
        password_field.send_keys(password)

    @allure.step("Нажатие кнопки login")
    def login_button(self):
        login_button = self.wait.until(EC.visibility_of_element_located((By.ID, self.data("selectors.login_page.login_btn"))))
        login_button.click()

    @allure.step("Проверка титульного названия главной страницы")
    def checking_title(self):
        products = self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, self.data("selectors.login_page.title_text"))))
        return products.text

    @allure.step("Проверка ошибки входа")
    def checking_error(self):
        error = self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, self.data("selectors.login_page.authentication error"))))
        return error.text


