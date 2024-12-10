from fastapi import FastAPI, HTTPException
from models import UserRegistration, UserToken, TokenAuthentication
from users_manager import UserManagerDB
from errors import UserNotFoundError, InvalidPassword

app = FastAPI()

user_manager = UserManagerDB()

# Registration
@app.post("/register")
async def register_user(user: UserRegistration) -> dict:
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
    except InvalidPassword:
        raise HTTPException(status_code=404, detail="Incorrect password")
    except Exception as e:
        raise HTTPException(status_code=410, detail=f"Error with login user: {e}")



# Token Verification
@app.post("/verify_token")
async def verify_token(user: TokenAuthentication) -> dict:
    try:
        is_valid = user_manager.authenticate_token(user.user_token, user.user_name)
        if is_valid:
            return {"valid": True}
        else:
            return {"valid": False}
    except UserNotFoundError:
        raise HTTPException(status_code=404, detail="User not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error verifying token: {e}")



