import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from DataProvider import DataProvider


class MainPage:
    def __init__(self, driver: WebDriver) ->None:
        self.url = DataProvider().get("url")
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    @allure.step("Перейти на сайт")
    def go(self):
        self.driver.get(self.url)

    @allure.step("Авторизация по логину и паролю")
    def login_authorization(self, standart, password):
        login_field = self.wait.until(EC.visibility_of_element_located((By.ID, "user-name")))
        login_field.send_keys(standart)

        password_field = self.wait.until(EC.visibility_of_element_located((By.ID, "password")))
        password_field.send_keys(password)

        login_button = self.wait.until(EC.visibility_of_element_located((By.ID, "login-button")))
        login_button.click()

    @allure.step("Проверка перехода на вкладку продукты")
    def checking_products(self):
        products = self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".title")))
        return products.text

    @allure.step("Проверка ошибки входа")
    def checking_error(self):
        error = self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "h3[data-test='error']")))
        return error.text

    @allure.step("Клик по кнопке login")
    def click_login_button(self):
        login_button = self.wait.until(EC.visibility_of_element_located((By.ID, "login-button")))
        login_button.click()

