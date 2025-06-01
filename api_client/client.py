from typing import Union

import allure
import requests

from models.pet_models import LoginModel, LoginResponseModel, CreatePetModel, PetResponseModel, GetPetsListModel, \
    PetListResponseModel, NegativeLoginResponseModel, NegativePetsListModel
from utils.validate_response import ValidateResponse
# from dotenv import load_dotenv


class ClientApi:
    def __init__(self):
        self.base_url = 'http://34.141.58.52:8000/'
        self.session = self._initialize_session()

    @staticmethod
    def _initialize_session():
        return requests.Session()

    def request(self, method: str, url: str, json=None, headers: str = None):
        response = self.session.request(method=method,
                                        url=self.base_url + url,
                                        headers=headers,
                                        json=json)
        return response


class Client(ClientApi):
    def __init__(self):
        super().__init__()

    @allure.step('POST /login')
    def login(self, request: LoginModel, expected_model: Union[LoginResponseModel, NegativeLoginResponseModel],
              status_code: int = 200):
        response = self.request(method='post', url='login', json=request.model_dump())
        return ValidateResponse.validate_response(response=response, model=expected_model, status_code=status_code)

    @allure.step('POST /pet')
    def post_pet(self, request: CreatePetModel, expected_model: PetResponseModel, headers, status_code: int = 200):
        response = self.request(method='post', url='pet', headers=headers, json=request.model_dump())
        return ValidateResponse.validate_response(response=response, model=expected_model,
                                                  status_code=status_code)

    @allure.step('POST /pets')
    def get_pets_list(self, request: GetPetsListModel,
                      expected_model: Union[PetListResponseModel, NegativePetsListModel],
                      headers, status_code: int = 200):
        response = self.request(method='post', url='pets', headers=headers, json=request.model_dump())
        return ValidateResponse.validate_response(response=response, model=expected_model,
                                                  status_code=status_code)

    @allure.step('DELETE /pet')
    def delete_pet(self, pet_id: int, headers, status_code: Union[int, list] = 200):
        response = self.request(method='delete', url=f'pet/{pet_id}', headers=headers)
        return ValidateResponse.validate_status_code(response=response, expected_status_code=status_code)

    @allure.step('PATCH /pet')
    def update_pet(self, request: CreatePetModel, expected_model: PetResponseModel, headers,
                   status_code: int = 200):
        response = self.request(method='patch', url='pet', headers=headers, json=request.model_dump())
        return ValidateResponse.validate_response(response=response, model=expected_model,
                                                  status_code=status_code)

    @allure.step('GET /pet')
    def get_pet(self, pet_id: int, headers, status_code: int = 200):
        response = self.request(method='get', url=f'pet/{pet_id}', headers=headers)
        return ValidateResponse.validate_status_code(response=response, expected_status_code=status_code)

    @allure.step('PUT /pet/like')
    def like_pet(self, pet_id: int, headers, status_code: int = 200):
        response = self.request(method='put', url=f'pet/{pet_id}/like', headers=headers)
        return ValidateResponse.validate_status_code(response=response, expected_status_code=status_code)