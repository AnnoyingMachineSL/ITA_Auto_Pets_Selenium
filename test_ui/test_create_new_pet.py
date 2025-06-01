import time
import allure
import pytest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions

from api_client.client import Client
from models.pet_models import LoginModel, LoginResponseModel
from utils.generator import random_name
from utils.config import LoginPageSecond, LoginPageConfig
from locators.login_page import LoginLocators
from locators.new_pet_page import CreatePetLocators


@allure.title('[Positive Test] Add pet')
@allure.severity(allure.severity_level.CRITICAL)
class TestCreateNewPet:

    @pytest.mark.positive
    @allure.title('Add pet by correct data')
    @pytest.mark.parametrize('email', [LoginPageSecond.LOGIN])
    @pytest.mark.parametrize('password', [LoginPageSecond.PASSWORD])
    @pytest.mark.parametrize('pet_type, age, gender', [('dog', '1', 'male'), ('cat', '2', 'female'),
                                                       ('reptile', '3', 'male'), ('hamster', '1', 'female')])
    def test_add_pet(self, driver, pet_type: str, age: str, gender: str, email: str, password: str):
        with allure.step(f'Log in by {LoginPageSecond.LOGIN}'):
            driver.get(LoginPageConfig.LOGIN_PAGE_URL)

            WebDriverWait(driver, 1).until(
                expected_conditions.visibility_of_element_located(
                    LoginLocators.LOGIN_FIELD)).send_keys(LoginPageSecond.LOGIN)

            WebDriverWait(driver, 1).until(
                expected_conditions.visibility_of_element_located(
                    LoginLocators.PASSWORD_FIELD)).send_keys(LoginPageSecond.PASSWORD)
            driver.find_element(*LoginLocators.LOGIN_LOGO).click()

            WebDriverWait(driver, 1).until(
                expected_conditions.visibility_of_element_located(
                    LoginLocators.SUBMIT_BUTTON)).click()

        with allure.step('Click Add Pet button'):
            WebDriverWait(driver, 1).until(
                expected_conditions.visibility_of_element_located(
                    CreatePetLocators.CREATE_PET_BUTTON)).click()

        with allure.step('Fill pet name field'):
            WebDriverWait(driver, 1).until(
                expected_conditions.visibility_of_element_located(
                    CreatePetLocators.NAME_FIELD)).send_keys(random_name())

        with allure.step(f'Fill pet age field by {age}'):
            WebDriverWait(driver, 1).until(
                expected_conditions.visibility_of_element_located(
                    CreatePetLocators.AGE_FIELD)).send_keys(age)

        with allure.step(f'Click on pet type dropdown'):
            WebDriverWait(driver, 1).until(
                expected_conditions.visibility_of_element_located(
                    CreatePetLocators.TYPE_DROPDOWN)).click()

        with allure.step(f'Fill pet type field by {pet_type}'):
            WebDriverWait(driver, 1).until(
                expected_conditions.visibility_of_element_located(
                    CreatePetLocators.PET_TYPES[pet_type])).click()

        with allure.step(f'Click on pet gender dropdown'):
            WebDriverWait(driver, 1).until(
                expected_conditions.visibility_of_element_located(
                    CreatePetLocators.GENDER_FIELD)).click()

        with allure.step(f'Fill pet gender field by {gender}'):
            WebDriverWait(driver, 1).until(
                expected_conditions.visibility_of_element_located(
                    CreatePetLocators.GENDERS[gender])).click()

        with allure.step('Click submit button'):
            WebDriverWait(driver, 1).until(
                expected_conditions.visibility_of_element_located(
                    CreatePetLocators.SUBMIT_BUTTON)).click()

        with allure.step('Get pet id from URL'):
            time.sleep(1)
            pet_id = int(driver.current_url.split('/')[5])


        with allure.step('[POST /login] Authorization'):
            authorization_response = Client().login(request=LoginModel(email=email, password=password),
                                                    expected_model=LoginResponseModel())

        with allure.step('Create API request to check new pet'):
            headers = dict(Authorization=f'Bearer {authorization_response.token}')
            Client().get_pet(pet_id=pet_id, headers=headers)


