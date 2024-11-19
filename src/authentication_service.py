from fastapi import FastAPI, HTTPException

auth_app = FastAPI()



# Registration
@auth_app.post("/register")
async def register_user(user_name:str, user_password:str):
    pass



# Login
auth_app.post("/login")
async def login(user_name:str, password:str):
    pass




# Token Verification
auth_app.get("/verify_token")
async def verify_token(user_token:str):
    pass