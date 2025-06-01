import allure
import pytest

from utils import generator
from api_client.client import Client
from utils.config import LoginPageSecond, LoginPageConfig
from models.pet_models import PetResponseModel, LoginResponseModel, LoginModel, CreatePetModel, GetPetsListModel, \
    PetListResponseModel, PetInfoResponseModel, NegativeLoginResponseModel, NegativePetsListModel
from utils.validate_response import ValidateResponse


@allure.title('[Positive] Api Tests')
class TestApi:

    @allure.title('[Api test] Authorization')
    @pytest.mark.positive
    @pytest.mark.API
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.parametrize('email', [LoginPageConfig.LOGIN])
    @pytest.mark.parametrize('password', [LoginPageSecond.PASSWORD])
    def test_login(self, email: str, password: str):
        with allure.step(f'Create LoginModel by email:{email}'):
            login_model = LoginModel(email=email, password=password)
        with allure.step(f'Log in by models: {login_model} and {LoginResponseModel}'):
            response = Client().login(request=login_model, expected_model=LoginResponseModel())
        return response

    @allure.title('[Api test] Post pet')
    @pytest.mark.positive
    @pytest.mark.API
    @pytest.mark.parametrize('email', [LoginPageSecond.LOGIN])
    @pytest.mark.parametrize('password', [LoginPageSecond.PASSWORD])
    @pytest.mark.parametrize('name', ['aas', 'bbs', 'qwe'])
    @pytest.mark.parametrize('pet_type', ['cat'])
    @pytest.mark.parametrize('age', ['1', '2'])
    @pytest.mark.parametrize('gender', ['male', 'female'])
    def test_post_pet(self, email: str, password: str,
                      name: str, pet_type: str, age: int, gender: str):

        with allure.step(f'Create LoginModel by email:{email}'):
            login_model = LoginModel(email=email, password=password)
        with allure.step(f'Log in by models: {login_model} and {LoginResponseModel}'):
            authorization_response = Client().login(request=login_model, expected_model=LoginResponseModel())
        with allure.step(f'Create PetModel with :{authorization_response.id}'):
            headers = dict(Authorization=f'Bearer {authorization_response.token}')
            pet_info_model = CreatePetModel(
                id=0,
                name=name,
                type=pet_type,
                age=age,
                gender=gender,
                owner_id=authorization_response.id)
        with allure.step(f'Get response after posting new pet'):
            created_pet_response = Client().post_pet(request=pet_info_model,
                                                     expected_model=PetResponseModel(),
                                                     headers=headers)
        return created_pet_response

    @allure.title('[Api test] Get pets list')
    @pytest.mark.positive
    @pytest.mark.API
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.dependency(name='test_get_pets_list')
    @pytest.mark.dependency(depends='test_post_pet')
    @pytest.mark.parametrize('email', [LoginPageSecond.LOGIN])
    @pytest.mark.parametrize('password', [LoginPageSecond.PASSWORD])
    @pytest.mark.parametrize('len_pet_list', [5])
    def test_get_pets_list(self, email: str, password: str, len_pet_list: int, user_id: int = None):
        with allure.step(f'Create LoginModel by email:{email}'):
            login_model = LoginModel(email=email, password=password)
        with allure.step(f'Log in by models: {login_model} and {LoginResponseModel}'):
            authorization_response = Client().login(request=login_model, expected_model=LoginResponseModel())

        with allure.step(f'Create PetsListModel with :{authorization_response.id}'):
            headers = dict(Authorization=f'Bearer {authorization_response.token}')
            pets_list_model = GetPetsListModel(
                skip=0,
                num=len_pet_list,
                user_id=authorization_response.id if not user_id else user_id)

        with allure.step(f'Get pets list'):
            pets_list_response = Client().get_pets_list(request=pets_list_model,
                                                        expected_model=PetListResponseModel(
                                                            list=[CreatePetModel(
                                                                id=None,
                                                                name=None,
                                                                type=None,
                                                                age=None,
                                                                gender=None,
                                                                owner_id=None,
                                                                pic='string',
                                                                owner_name='string',
                                                                likes_count=0,
                                                                liked_by_user=False)]),
                                                        headers=headers)
        return pets_list_response

    @allure.title('[Api test] Delete pet')
    @pytest.mark.positive
    @pytest.mark.API
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.dependency(depends='test_get_pets_list')
    @pytest.mark.parametrize('email', [LoginPageSecond.LOGIN])
    @pytest.mark.parametrize('password', [LoginPageSecond.PASSWORD])
    @pytest.mark.parametrize('len_pet_list', [15])
    def test_delete_pet(self, email: str, password: str, len_pet_list: int):
        with allure.step(f'Get list of pets id for user {email}'):
            pets_id_list = generator.extract_pet_id(self.test_get_pets_list(email, password, len_pet_list))
        with allure.step(f'Create LoginModel by email:{email}'):
            login_model = LoginModel(email=email, password=password)
        with allure.step(f'Log in by models: {login_model} and {LoginResponseModel}'):
            authorization_response = Client().login(request=login_model, expected_model=LoginResponseModel())
        headers = dict(Authorization=f'Bearer {authorization_response.token}')

        for pet_id in pets_id_list:
            with allure.step(f'Delete pet by id:{pet_id}'):
                Client().delete_pet(pet_id=pet_id, headers=headers)

    @allure.title('[Api test] Update pet info')
    @pytest.mark.positive
    @pytest.mark.API
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize('email', [LoginPageSecond.LOGIN])
    @pytest.mark.parametrize('password', [LoginPageSecond.PASSWORD])
    @pytest.mark.parametrize('len_pet_list', [3])
    @pytest.mark.parametrize('pet_name', ['Katana'])
    @pytest.mark.parametrize('pet_type', ['Sword'])
    @pytest.mark.parametrize('pet_age', [100])
    @pytest.mark.parametrize('pet_gender', ['Female'])
    def test_update_pet_info(self, email: str, password: str, len_pet_list: int,
                             pet_name: str, pet_type: str, pet_age: int, pet_gender: str):

        with allure.step(f'Get list of pets id for user {email}'):
            pets_id_list = generator.extract_pet_id(self.test_get_pets_list(email, password, len_pet_list))
        with allure.step(f'Create LoginModel by email:{email}'):
            login_model = LoginModel(email=email, password=password)
        with allure.step(f'Log in by models: {login_model} and {LoginResponseModel}'):
            authorization_response = Client().login(request=login_model, expected_model=LoginResponseModel())
        headers = dict(Authorization=f'Bearer {authorization_response.token}')

        for pet_id in pets_id_list:
            with allure.step(f'Create New pet model for update information'):
                pet_info_model = CreatePetModel(id=pet_id, name=pet_name,
                                                type=pet_type, age=pet_age,
                                                gender=pet_gender, owner_id=authorization_response.id)
            with allure.step(f'Update information about pet by new model: {pet_info_model}'):
                Client().update_pet(request=pet_info_model,
                                    expected_model=PetResponseModel(),
                                    headers=headers)
            with allure.step('Get actual information about pet after updating'):
                actual_pet_data = Client().get_pet(pet_id=pet_id, headers=headers)
            with allure.step('Create expected information model for pet'):
                expected_pet_data = PetInfoResponseModel(pet=pet_info_model, comments=[])
            with allure.step(f'Comparing information between actual and expected pet information models'):
                ValidateResponse.validate_response(response=actual_pet_data, model=expected_pet_data)

    @allure.title('[Api test] Like pet')
    @pytest.mark.positive
    @pytest.mark.API
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.parametrize('email', [LoginPageSecond.LOGIN])
    @pytest.mark.parametrize('password', [LoginPageSecond.PASSWORD])
    @pytest.mark.parametrize('len_pet_list', [10])
    def test_like_pet(self, email: str, password: str, len_pet_list: int):
        with allure.step(f'Get list of pets id for user {email}'):
            pets_id_list = generator.extract_not_liked_pet_id(self.test_get_pets_list(email, password, len_pet_list))
        with allure.step(f'Create LoginModel by email:{email}'):
            login_model = LoginModel(email=email, password=password)
        with allure.step(f'Log in by models: {login_model} and {LoginResponseModel}'):
            authorization_response = Client().login(request=login_model, expected_model=LoginResponseModel())
        headers = dict(Authorization=f'Bearer {authorization_response.token}')

        for pet_id in pets_id_list:
            with allure.step(f'Like pet by id:{pet_id}'):
                Client().like_pet(pet_id=pet_id, headers=headers)


@allure.title('[Negative] Api Tests')
class TestApiNegative:

    @allure.title('[Api test] Authorization by incorrect data')
    @pytest.mark.negative
    @pytest.mark.API
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.parametrize('email', [LoginPageSecond.LOGIN, '', '!@#', '@mail.com', 'qwe@qwe'])
    @pytest.mark.parametrize('password', ['', 'a', 'zxc', '123123'])
    def test_negative_login_incorrect_data(self, email: str, password: str):
        with allure.step(f'Create LoginModel by email:{email}'):
            login_model = LoginModel(email=email, password=password)
        with allure.step(f'Log in by models: {login_model} and {NegativeLoginResponseModel}'):
            response = Client().login(request=login_model, expected_model=NegativeLoginResponseModel(), status_code=400)
        return response

    @allure.title('[Api test] Get pets list by incorrect len')
    @pytest.mark.negative
    @pytest.mark.API
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize('email', [LoginPageSecond.LOGIN])
    @pytest.mark.parametrize('password', [LoginPageSecond.PASSWORD])
    @pytest.mark.parametrize('len_pet_list', ['qwe', '', -2, "!@#!@#"])
    def test_negative_pets_list_incorrect_len(self, email: str, password: str, len_pet_list: int):
        with allure.step(f'Create LoginModel by email:{email}'):
            login_model = LoginModel(email=email, password=password)
        with allure.step(f'Log in by models: {login_model} and {LoginResponseModel}'):
            authorization_response = Client().login(request=login_model, expected_model=LoginResponseModel())
        headers = dict(Authorization=f'Bearer {authorization_response.token}')

        with allure.step(f'Create new PetListModel by len:{len_pet_list}'):
            pets_list_model = GetPetsListModel(skip=0, num=len_pet_list, user_id=authorization_response.id)

        with allure.step('Get response using incorrect pet list len'):
            pets_list_response = Client().get_pets_list(request=pets_list_model, expected_model=NegativePetsListModel(),
                                                        headers=headers, status_code=422)
        return pets_list_response

    @allure.title('[Api test] Delete pet by incorrect id')
    @pytest.mark.negative
    @pytest.mark.API
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize('email', [LoginPageSecond.LOGIN])
    @pytest.mark.parametrize('password', [LoginPageSecond.PASSWORD])
    @pytest.mark.parametrize('pet_id', ['', 'a', -4, '!@#!@#'])
    def test_negative_delete_pet(self, email: str, password: str, pet_id):
        with allure.step(f'Create LoginModel by email:{email}'):
            login_model = LoginModel(email=email, password=password)
        with allure.step(f'Log in by models: {login_model} and {LoginResponseModel}'):
            authorization_response = Client().login(request=login_model, expected_model=LoginResponseModel())
        headers = dict(Authorization=f'Bearer {authorization_response.token}')
        with allure.step(f'Try to delete pet using incorrect id:{pet_id}'):
            Client().delete_pet(pet_id=pet_id, headers=headers, status_code=[422, 405])

    @allure.title('Delete pet by id from other user')
    @pytest.mark.negative
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.parametrize('first_email', [LoginPageConfig.LOGIN])
    @pytest.mark.parametrize('first_password', [LoginPageConfig.PASSWORD])
    @pytest.mark.parametrize('second_email', [LoginPageSecond.LOGIN])
    @pytest.mark.parametrize('second_password', [LoginPageSecond.PASSWORD])
    @pytest.mark.parametrize('len_pet_list', [2])
    def test_delete_pet_from_someone_account(self, first_email: str, first_password: str,
                                             second_email: str, second_password: str, len_pet_list: int):
        with allure.step(f'Autorization by second user: {second_email}'):
            second_user_authorization_data = TestApi().test_login(email=second_email, password=second_password)

        with allure.step(f'Get pet list using {second_email} id'):
            pets_id_list = generator.extract_pet_id(TestApi().test_get_pets_list(email=first_email, password=first_password,
                                                                                 len_pet_list=len_pet_list,
                                                                                 user_id=second_user_authorization_data.id))
        with allure.step(f'Create LoginModel for first user :{first_email}'):
            login_model = LoginModel(email=first_email, password=first_password)
        with allure.step(f'Log in by models: {login_model} and {LoginResponseModel}'):
            authorization_response = Client().login(request=login_model, expected_model=LoginResponseModel())
        headers = dict(Authorization=f'Bearer {authorization_response.token}')

        for pet_id in pets_id_list:
            with allure.step(f'Try to delete {second_email} pets from account {first_email}'):
                Client().delete_pet(pet_id=pet_id, headers=headers, status_code=403)