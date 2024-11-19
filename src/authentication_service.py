from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


app = FastAPI()

# Registration
@app.post("/register")
async def register_user(user_name:str, user_password:str):
    pass



# Login
@app.post("/login")
async def login(user_name:str, password:str):
    pass

# Token Verification
@app.get("/verify_token")
async def verify_token(user_token:str):
    pass




############### Example message endpoint ###############

class UserRequest(BaseModel):
    user: str

# Example message endpoint
@app.post("/example_message_endpoint")
async def verify_token(user_request: UserRequest):
    return {"example_message": f"{user_request.user}: blabla" }

