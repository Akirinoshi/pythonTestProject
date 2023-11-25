from typing import Optional
from pydantic import BaseModel


class UsersSignUpModel(BaseModel):
    email: str
    password: str


class UsersSignInModel(BaseModel):
    email: str
    password: str
