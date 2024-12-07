from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from models import UserRegistration, UserToken
from users_manager import UserManagerDB

app = FastAPI()

user_manager = UserManagerDB()

# Registration
@app.post("/register")
async def register_user(user: UserRegistration):
    try:
        response = user_manager.register_user(user.user_name, user.user_password)
        return {"message": response}
    except Exception as e:
        raise HTTPException(status_code=410, detail=f"Error occurs when try to register user: {e}")



# Login
@app.post("/login")
async def login(user: UserRegistration) -> UserToken:
    try:
        user_token = user_manager.login_user(user.user_name, user.user_password)
        user_token_object = UserToken(user_token = user_token)
        return user_token_object
    except Exception as e:
        raise HTTPException(status_code=410, detail=f"Error occurs when try to login user: {e}")



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

