from pydantic import BaseModel
import time
from typing import List


class SendMessage(BaseModel):
    SrcName: str
    message: List[str]
    DstName: str

class ReceiveMessage(BaseModel):
    From: str
    message: List[str]