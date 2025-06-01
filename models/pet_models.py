from typing import Optional, Union
import json
from pydantic import BaseModel, Field

#Components
class NegativePetsListModelComponents(BaseModel):
    loc: Optional[list]
    msg: Optional[str]
    type: Optional[str]
    ctx: Optional[dict]


# Request models
class LoginModel(BaseModel):
    email: Optional[str]
    password: Optional[str]


class CreatePetModel(BaseModel):
    id: Optional[int]
    name: Optional[str]
    type: Optional[str]
    age: Optional[int]
    gender: Optional[str]
    owner_id: Optional[int]
    pic: Optional[str] = 'string'
    owner_name: Optional[str] = 'string'
    likes_count: Optional[int] = 0
    liked_by_user: Optional[bool] = False


class GetPetsListModel(BaseModel):
    skip: Optional[int] = 0
    num: Optional[Union[int, str]]
    user_id: Optional[int]


# Response models
class LoginResponseModel(BaseModel):
    token: Optional[str] = None
    email: Optional[str] = None
    id: Optional[int] = None


class PetResponseModel(BaseModel):
    id: Optional[int] = None


class PetListResponseModel(BaseModel):
    list: Optional[list[CreatePetModel]]
    total: Optional[int] = None

class PetInfoResponseModel(BaseModel):
    pet: CreatePetModel
    comments: Optional[list]


#Negative response models

class NegativeLoginResponseModel(BaseModel):
    detail: Optional[str] = 'Username is taken or pass issue'


class NegativePetsListModel(BaseModel):
    detail: Optional[list] = [NegativePetsListModelComponents]