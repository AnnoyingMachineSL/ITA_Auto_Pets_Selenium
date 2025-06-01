import time
import allure
import pytest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions

from utils.config import LoginPageSecond, LoginPageConfig
from locators.login_page import LoginLocators
from locators.main_page import MainPageLocators


@allure.title('[Positive test] Delete Pet')
@allure.severity(allure.severity_level.NORMAL)
class TestDeletePet:

    @pytest.mark.positive
    @allure.title('Delete pet from profile page')
    @pytest.mark.parametrize('email', [LoginPageSecond.LOGIN])
    @pytest.mark.parametrize('password', [LoginPageSecond.PASSWORD])
    def test_delete_pet(self, driver, email: str, password: str):
        with allure.step(f'Log in by {LoginPageSecond.LOGIN}'):
            driver.get(LoginPageConfig.LOGIN_PAGE_URL)

            WebDriverWait(driver, 10).until(
                expected_conditions.visibility_of_element_located(
                    LoginLocators.LOGIN_FIELD)).send_keys(LoginPageSecond.LOGIN)

            WebDriverWait(driver, 10).until(
                expected_conditions.visibility_of_element_located(
                    LoginLocators.PASSWORD_FIELD)).send_keys(LoginPageSecond.PASSWORD)
            driver.find_element(*LoginLocators.LOGIN_LOGO).click()

            WebDriverWait(driver, 10).until(
                expected_conditions.visibility_of_element_located(
                    LoginLocators.SUBMIT_BUTTON)).click()

        with allure.step('Search all delete buttons'):
            time.sleep(2)
            lst = driver.find_elements(*MainPageLocators.DELETE_BUTTONS)

        with allure.step('Click on delete button'):
           lst[0].click()

        with allure.step('Confirm pet deletion'):
            WebDriverWait(driver, 10).until(
                expected_conditions.visibility_of_element_located(
                    MainPageLocators.CONFIRM_DELETE_BUTTON)).click()

        with allure.step('Search success delete message'):
            WebDriverWait(driver, 10).until(
                expected_conditions.visibility_of_element_located(
                    MainPageLocators.SUCCESS_DELETE_MESSAGE))


