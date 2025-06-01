import re
import time
import allure
import pytest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from utils.config import LoginPageConfig
from locators.login_page import LoginLocators


@allure.title('[Positive] Login Test')
@allure.severity(allure.severity_level.CRITICAL)
class TestLogin:
    @pytest.mark.positive  # Маркировка тестов. Использся pytest -m negative запустятся только тесты с маркой negative
    @allure.title('Login with correct data')
    @allure.description('Log in like existing user with correct login/password')
    def test_login(self, driver):
        with allure.step('Open login page'):
            driver.get(LoginPageConfig.LOGIN_PAGE_URL)

        with allure.step('Fill login field'):
            WebDriverWait(driver, 1).until(
                expected_conditions.visibility_of_element_located(
                    LoginLocators.LOGIN_FIELD)).send_keys(LoginPageConfig.LOGIN)

        with allure.step('Fill password field'):
            WebDriverWait(driver, 1).until(
                expected_conditions.visibility_of_element_located(
                    LoginLocators.PASSWORD_FIELD)).send_keys(LoginPageConfig.PASSWORD)
            driver.find_element(*LoginLocators.LOGIN_LOGO).click()

        with allure.step('Click on Submit button'):
            WebDriverWait(driver, 1).until(
                expected_conditions.visibility_of_element_located(
                    LoginLocators.SUBMIT_BUTTON)).click()

        time.sleep(2)
        assert driver.current_url == LoginLocators.AFTER_LOGIN_URL


@allure.title('[Negative] Login Test')
@allure.severity(allure.severity_level.CRITICAL)
class TestLoginNegative:
    @pytest.mark.negative
    @allure.title('Try to login by incorrect data')
    @pytest.mark.parametrize('email, password', [('a', 'qwe123'), ('', 'qwe123'), ('@gmail.com', ''), ('', '')])
    def test_login_invalid_email(self, driver, email, password):

        with allure.step('Open login page'):
            driver.get(LoginPageConfig.LOGIN_PAGE_URL)

        with allure.step(f'Fill login field with {email}'):
            WebDriverWait(driver, 1).until(
                expected_conditions.visibility_of_element_located(
                    LoginLocators.LOGIN_FIELD)).send_keys(email)

        with allure.step(f'Fill password field with {password}'):
            WebDriverWait(driver, 1).until(
                expected_conditions.visibility_of_element_located(
                    LoginLocators.PASSWORD_FIELD)).send_keys(password)
            driver.find_element(*LoginLocators.LOGIN_LOGO).click()

        with allure.step('Click on Submit botton'):
            WebDriverWait(driver, 1).until(
                expected_conditions.visibility_of_element_located(
                    LoginLocators.SUBMIT_BUTTON)).click()

        if len(re.findall('.*@mail.com', email)) == 0:
            WebDriverWait(driver, 1).until(
                expected_conditions.visibility_of_element_located(
                    LoginLocators.EMPTY_LOGIN_ERROR_MESSAGE))

        if len(password) == 0:
            WebDriverWait(driver, 1).until(
                expected_conditions.visibility_of_element_located(
                    LoginLocators.EMPTY_PASSWORD_ERROR_MESSAGE))

