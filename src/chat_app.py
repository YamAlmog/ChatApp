from fastapi import FastAPI, HTTPException
from models import MessagesDetails
from message_manager import MessageManagerDB
from errors import MessageManagerException
import datetime
import httpx
from typing import Dict, List

# Init up
app = FastAPI()

msg_manager = MessageManagerDB()


AUTH_APP_URL="http://authentication_service:8000"

async def validate_token(token: str, user_name: str):
    url = f"{AUTH_APP_URL}/verify_token"
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json={"user_token": token, "user_name": user_name})
            response.raise_for_status() # Raise HTTP error for 4xx/5xx responses
            return response.json()["valid"]
    except httpx.HTTPStatusError as e:
        # Extract the error details from the response if available
        if e.response is not None:
            raise HTTPException(
                status_code=e.response.status_code,
                detail=e.response.json().get("detail", "Unknown error from authentication service.")
            )
        raise HTTPException(status_code=500, detail="Authentication service error occurred.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")


@app.post("/send_message")
async def send_message(send_details:MessagesDetails, token:str) -> Dict[str,str]:
    try:
        is_valid = await validate_token(token, send_details.user_name)
        if not is_valid:
            raise HTTPException(status_code=403, detail = "Invalid or expired token.")
        time = str(datetime.datetime.now())
        msg_manager.insert_message_details(send_details, time)
        
        return {"message": "messages sent successfully"}
    except MessageManagerException as e:
        raise HTTPException(status_code=404, detail = str(e))
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail = f"Internal server error: {e}")
   


@app.get("/get_messages")
async def get_messages(user_name:str, token:str)-> List[Dict[str,str]]:
    try:
        is_valid = await validate_token(token, user_name)
        if not is_valid:
            raise HTTPException(status_code=403, detail = "Invalid or expired token.")
        return msg_manager.retrieve_messages_of_given_user(user_name)
        
    except MessageManagerException as e:
        raise HTTPException(status_code=404, detail = str(e))
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail = f"Internal server error: {e}")
    



