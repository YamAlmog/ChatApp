from fastapi import FastAPI, HTTPException
from models import SendMessage, ReceiveMessage
from message_manager import messageManagerDB
from errors import messageManagerException
import datetime
from typing import List
import requests

# Init up
app = FastAPI()

msg_manager = messageManagerDB()

AUTH_APP_URL="http://authentication_service:8000"


@app.post("/send_message")
async def send_message(sendDetails:SendMessage) -> str:
    try:
        src_name = sendDetails.SrcName
        dst_name = sendDetails.DstName
        msg = sendDetails.message
        time = str(datetime.datetime.now())
        
        msg_manager.insert_message_details(src_name, dst_name, msg, time)
        
        return {"message": "message sent successfully"}
    except messageManagerException as e:
        raise HTTPException(status_code=400, detail={e+time})
   


@app.get("/get_messages")
async def get_messages(user_name:str) -> List[ReceiveMessage]:
    try:
        return msg_manager.arrange_message_to_sent(user_name)
        
    except messageManagerException as e:
        raise HTTPException(status_code=400, detail=str(e))
    


@app.get("/example_send_request_to_get_example_message")
async def get_messages(user_name:str) -> str:
    print("=======>> sending request to generate token")
    response = requests.post(f"{AUTH_APP_URL}/example_message_endpoint", json={"user": user_name})
    
    return response.json()['example_message']
    

@app.get("/test_insert_messages")
async def test_insert_messages() -> dict:
    msg_manager.insert_messages_test()
    return {"message": "test messages inserted successfully"}
        

