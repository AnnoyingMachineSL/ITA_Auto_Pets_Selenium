import re
import time
import allure
import pytest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from locators.registration_page import RegistrationConfig
from utils.generator import random_email, random_password


@allure.title('[Positive] Login Test')
@allure.severity(allure.severity_level.CRITICAL)
class TestRegistration:
    @pytest.mark.positive
    @allure.title('Registration new user')
    @allure.description('Registration new user with random correct login/password')
    def test_registration(self, driver):
        with allure.step('Open login page'):
            driver.get(RegistrationConfig.REGISTRATION_BASE_URS)

        with allure.step('Fill login field'):
            WebDriverWait(driver, 1).until(
                expected_conditions.visibility_of_element_located(
                    RegistrationConfig.LOGIN_FIELD)).send_keys(random_email())

        password = random_password()

        with allure.step('Fill password field'):
            WebDriverWait(driver, 1).until(
                expected_conditions.visibility_of_element_located(
                    RegistrationConfig.PASSWORD_FIELD)).send_keys(password)
            driver.find_element(*RegistrationConfig.REGISTRATION_LOGO).click()

        with allure.step('Fill confirm password field'):
            WebDriverWait(driver, 1).until(
                expected_conditions.visibility_of_element_located(
                    RegistrationConfig.CONFIRM_PASSWORD_FIELD)).send_keys(password)
            driver.find_element(*RegistrationConfig.REGISTRATION_LOGO).click()

        with allure.step('Click on Submit button'):
            WebDriverWait(driver, 1).until(
                expected_conditions.visibility_of_element_located(
                    RegistrationConfig.SUBMIT_BUTTON)).click()

        time.sleep(2)
        assert driver.current_url == RegistrationConfig.AFTER_REGISTRATION_URL



@allure.title('[Negative Test] Registration')
@allure.severity(allure.severity_level.CRITICAL)
class TestRegistrationNegative:

    @pytest.mark.negative
    @allure.title('Incorrect email format')
    @pytest.mark.parametrize('email, password', [('a', 'qwe123'), ('', 'qwe123'), ('@gmail.com', 'qwe123')])
    @allure.description('Registration with incorrect email and expect an error message')
    def test_registration_invalid_email_format(self, driver, email, password):
        with allure.step('Open login page'):
            driver.get(RegistrationConfig.REGISTRATION_BASE_URS)

        with allure.step(f'Fill email field by {email}'):
            WebDriverWait(driver, 1).until(
                expected_conditions.visibility_of_element_located(
                    RegistrationConfig.LOGIN_FIELD)).send_keys(email)

        with allure.step(f'Fill password and confirm password field by {password}'):
            WebDriverWait(driver, 1).until(
                expected_conditions.visibility_of_element_located(
                    RegistrationConfig.PASSWORD_FIELD)).send_keys(password)
            driver.find_element(*RegistrationConfig.REGISTRATION_LOGO).click()

            WebDriverWait(driver, 1).until(
                expected_conditions.visibility_of_element_located(
                    RegistrationConfig.CONFIRM_PASSWORD_FIELD)).send_keys(password)
            driver.find_element(*RegistrationConfig.REGISTRATION_LOGO).click()


        with allure.step('Click Submit button'):
            WebDriverWait(driver, 1).until(
                expected_conditions.visibility_of_element_located(
                    RegistrationConfig.SUBMIT_BUTTON)).click()

        with allure.step('Check the error message'):
            WebDriverWait(driver, 1).until(
                expected_conditions.visibility_of_element_located(
                    RegistrationConfig.LOGIN_ERROR_MESSAGE))


    @pytest.mark.negative
    @allure.title('Difference between password and confirm password')
    @allure.description('Registration with incorrect email and expect an error message')
    def test_registration_with_different_passwords(self, driver):
        with allure.step('Open login page'):
            driver.get(RegistrationConfig.REGISTRATION_BASE_URS)

        with allure.step(f'Fill email field'):
            WebDriverWait(driver, 1).until(
                expected_conditions.visibility_of_element_located(
                    RegistrationConfig.LOGIN_FIELD)).send_keys(random_email())

        password = random_password()
        with allure.step(f'Fill password and confirm password field by {password} and {password[::-1]}'):
            WebDriverWait(driver, 1).until(
                expected_conditions.visibility_of_element_located(
                    RegistrationConfig.PASSWORD_FIELD)).send_keys(password)
            driver.find_element(*RegistrationConfig.REGISTRATION_LOGO).click()

            WebDriverWait(driver, 1).until(
                expected_conditions.visibility_of_element_located(
                    RegistrationConfig.CONFIRM_PASSWORD_FIELD)).send_keys(password[::-1])
            driver.find_element(*RegistrationConfig.REGISTRATION_LOGO).click()


        with allure.step('Click Submit button'):
            WebDriverWait(driver, 1).until(
                expected_conditions.visibility_of_element_located(
                    RegistrationConfig.SUBMIT_BUTTON)).click()

        with allure.step('Check the error message'):
            WebDriverWait(driver, 1).until(
                expected_conditions.visibility_of_element_located(
                    RegistrationConfig.ERROR_MESSAGE_IN_DIFFERENT_PASSWORDS))