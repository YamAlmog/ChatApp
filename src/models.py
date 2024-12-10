from pydantic import BaseModel
from typing import List


class MessagesDetails(BaseModel):
    user_name: str
    messages: List[str]
    destination_name: str


class UserRegistration(BaseModel):
    user_name: str
    user_password: str


class UserToken(BaseModel):
    user_token: str


class TokenAuthentication(UserToken):
    user_name : str