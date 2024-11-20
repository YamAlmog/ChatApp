from pydantic import BaseModel
from typing import List


class MessagesDetails(BaseModel):
    SourceName: str
    Messages: List[str]
    DestinationName: str

class ReceiveMessages(BaseModel):
    From: str
    Messages: List[str]