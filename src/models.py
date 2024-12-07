from pydantic import BaseModel
from typing import List


class MessagesDetails(BaseModel):
    source_name: str
    messages: List[str]
    destination_name: str


class ReceiveMessages(BaseModel):
    receive_from: str
    messages: List[str]


class UserRegistration(BaseModel):
    user_name: str
    user_password: str


class UserToken(BaseModel):
    user_token: str