from pydantic import BaseModel
import time


class SendMassage(BaseModel):
    SrcName: str
    Massage: str
    DstName: str

class ReceiveMassage(BaseModel):
    From: str
    Massage: str