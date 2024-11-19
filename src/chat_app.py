from fastapi import FastAPI
from models import SendMassage, ReceiveMassage

# Init up
app = FastAPI()


@app.post("/send_massage")
async def send_massage(sendDetails:SendMassage) -> None:
    return "send massage!"



@app.get("/fetch_massage")
async def get_massages() -> ReceiveMassage:
    pass