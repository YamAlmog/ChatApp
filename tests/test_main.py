from fastapi.testclient import TestClient
from chat_app import app as chat_app
from authentication_service import app as auth_app
import os
import psycopg2

DB_URL = os.getenv('DATABASE_URL')
CHAT_URL = os.getenv('CHAT_APP_URL')
AUTH_URL = os.getenv('CHAT_APP_URL')

chat_client = TestClient(chat_app)
auth_client = TestClient(auth_app)

USER1 = "Ran"
USER1_PASSWORD = "Ran123"
USER2 = "Dan"
USER1_PASSWORD = "Dan123"

def delete_user_from_db(user_name:str) -> None:
    query = "DELETE FROM registered_users WHERE user_name = %s;"
    try:
        with psycopg2.connect(DB_URL) as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, (user_name,))
                print(f"==============>>>> Delete user: {user_name} from registered_users table")
        
    except Exception as e:
        raise Exception(f"Error while try delete user details from registered_users: {e}")
    

# test registration function
def test_registration() -> None:
    delete_user_from_db(USER1)
    new_user = {"user_name": USER1, "user_password": USER1_PASSWORD}
    response = auth_client.post("/register", json=new_user)
    assert response.status_code == 200
    assert response.json() == {"message": "User successfully registered"}


# test login function and verify token
def test_login() -> None:
    global user_1_token
    new_user = {"user_name": USER1, "user_password": USER1_PASSWORD}
    response = auth_client.post("/login", json=new_user)
    assert response.status_code == 200
    
    user_1_token = response.json()['user_token']
    verify_token_response = auth_client.post("/verify_token", json={'user_token': user_1_token, 'user_name': USER1})
    assert verify_token_response.status_code == 200


def test_send_message() -> None:
    global user_1_token
    message_details = {'user_name': USER1, 'messages': ['Hi, how are you?'], 'destination_name': USER2}
    response = chat_client.post("/send_message", json = message_details, params= {'token': user_1_token})
    assert response.status_code == 200
    assert response.json() == {"message": "messages sent successfully"}


def test_get_message():
    pass