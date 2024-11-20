from fastapi import FastAPI, HTTPException
from models import MessagesDetails, ReceiveMessages
from message_manager import MessageManagerDB
from errors import MessageManagerException
import datetime
from typing import List
import requests

# Init up
app = FastAPI()

msg_manager = MessageManagerDB()

AUTH_APP_URL="http://authentication_service:8000"


@app.post("/send_message")
async def send_message(send_details:MessagesDetails):
    try:
        time = str(datetime.datetime.now())
        
        msg_manager.insert_message_details(send_details, time)
        
        return {"message": "messages sent successfully"}
    except MessageManagerException as e:
        raise HTTPException(status_code=400, detail=(e))
   


@app.get("/get_messages")
async def get_messages(user_name:str):
    try:
        return msg_manager.retrieve_messages_of_given_user(user_name)
        
    except MessageManagerException as e:
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
        

