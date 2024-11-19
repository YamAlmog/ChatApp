from fastapi import FastAPI, HTTPException
from models import SendMessage, ReceiveMessage
from message_manager import messageManager
from errors import messageManagerException
import datetime
from typing import List
# Init up
app = FastAPI()

msg_manager = messageManager()

@app.post("/send_message")
async def send_message(sendDetails:SendMessage) -> None:
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