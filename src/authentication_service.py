from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from users_manager import UserManagerDB

app = FastAPI()

user_manager = UserManagerDB

# Registration
@app.post("/register")
async def register_user(user_name:str, user_password:str):
    try:
        comment = user_manager.register_user(user_name, user_password)
        return {"message": comment}
    except Exception as e:
        raise HTTPException(status_code=410, detail=f"Error occurs when try to register user: {e}")



# Login
@app.post("/login")
async def login(user_name:str, password:str):
    try:
        user_token = user_manager.login_user(user_name, password)
        return {"User token:", user_token}
    except Exception as e:
        raise HTTPException(status_code=410, detail=f"Error occurs when try to register user: {e}")



# Token Verification
@app.get("/verify_token")
async def verify_token(user_token:str, user_name:str):
    pass




############### Example message endpoint ###############

class UserRequest(BaseModel):
    user: str

# Example message endpoint
@app.post("/example_message_endpoint")
async def example_message_endpoint(user_request: UserRequest):
    return {"example_message": f"{user_request.user}: blabla" }

