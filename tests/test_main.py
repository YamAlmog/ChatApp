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
USER2_PASSWORD = "Dan123"


def delete_user_from_db(user_name: str) -> None:
    query = "DELETE FROM registered_users WHERE user_name = %s;"
    try:
        with psycopg2.connect(DB_URL) as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, (user_name,))
                print(f"==============>>>> Delete user: {user_name} from registered_users table")

    except Exception as e:
        raise Exception(f"Error while try delete user details from registered_users: {e}")


def clean_db() -> None:
    clear_registered_users_query = "TRUNCATE TABLE registered_users;"
    clear_login_users_query = "TRUNCATE TABLE login_users;"
    clear_chat_messages_query = "TRUNCATE TABLE chat_messages;"
    try:
        with psycopg2.connect(DB_URL) as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    clear_registered_users_query,
                )
                print("-----------Empty registered_users table-----------")
                cursor.execute(
                    clear_login_users_query,
                )
                print("-----------Empty login_users table-----------")
                cursor.execute(
                    clear_chat_messages_query,
                )
                print("-----------Empty chat_messages table-----------")

    except Exception as e:
        raise Exception(f"Error while try delete user details from registered_users: {e}")


clean_db()

# -------------------------------------------- ____ registration tests ____ --------------------------------------------
# test registration function
def test_registration() -> None:
    new_user = {"user_name": USER1, "user_password": USER1_PASSWORD}
    response = auth_client.post("/register", json=new_user)
    assert response.status_code == 200
    assert response.json() == {"message": "User successfully registered"}


# test register user with InvalidUserName
def test_registration_with_InvalidUserName() -> None:
    new_user = {"user_name": USER1, "user_password": USER1_PASSWORD}
    response = auth_client.post("/register", json=new_user)
    assert response.status_code == 404
    assert response.json() == {
        "detail": "This username is already in use, please choose another name."
    }


# -------------------------------------------- ____ login tests ____ --------------------------------------------
# test login endpoint and verify token
def test_login() -> None:
    global user_1_token
    new_user = {"user_name": USER1, "user_password": USER1_PASSWORD}
    response = auth_client.post("/login", json=new_user)
    assert response.status_code == 200
    user_1_token = response.json()['user_token']


# test login with UnregisteredUser
def test_login_with_UnregisteredUser() -> None:
    new_user = {"user_name": USER2, "user_password": USER1_PASSWORD}
    response = auth_client.post("/login", json=new_user)
    assert response.status_code == 404
    assert response.json() == {"detail": "Unregistered user, Please sign up first"}


# test login with InvalidPassword
def test_login_with_InvalidPassword() -> None:
    new_user = {"user_name": USER1, "user_password": USER2_PASSWORD}
    response = auth_client.post("/login", json=new_user)
    assert response.status_code == 404
    assert response.json() == {"detail": "You entered an incorrect password"}


# -------------------------------------------- ____ verify token tests ____ --------------------------------------------
# test verify token endpoint
def test_verify_token() -> None:
    # Correct token
    global user_1_token
    verify_token_response = auth_client.post(
        "/verify_token", json={'user_token': user_1_token, 'user_name': USER1}
    )
    assert verify_token_response.status_code == 200
    assert verify_token_response.json() == {"valid": True}
    # Wrong token
    verify_token_response = auth_client.post(
        "/verify_token", json={'user_token': "aaa1222", 'user_name': USER1}
    )
    assert verify_token_response.status_code == 200
    assert verify_token_response.json() == {"valid": False}


# test verify token UserNotFoundError
def test_verify_token_UserNotFoundError() -> None:
    global user_1_token
    verify_token_response = auth_client.post(
        "/verify_token", json={'user_token': user_1_token, 'user_name': USER2}
    )
    assert verify_token_response.status_code == 404
    assert verify_token_response.json() == {
        "detail": "Unidentified user, not registered or not logged in"
    }


# -------------------------------------------- ____ send message tests ____ --------------------------------------------
# test send message endpoint
def test_send_message() -> None:
    global user_1_token
    message_details = {
        'user_name': USER1,
        'messages': ['Hi, how are you?'],
        'destination_name': USER2,
    }
    response = chat_client.post(
        "/send_message", json=message_details, params={'token': user_1_token}
    )
    assert response.status_code == 200
    assert response.json() == {"message": "messages sent successfully"}


# test send message with invalid token
def test_send_message_with_invalid_token() -> None:
    message_details = {
        'user_name': USER1,
        'messages': ['Hi, how are you?'],
        'destination_name': USER2,
    }
    response = chat_client.post("/send_message", json=message_details, params={'token': 'aaaaa'})
    assert response.status_code == 403
    assert response.json() == {"detail": "Invalid or expired token."}


# test send message with not found user_name
def test_send_message_with_not_found_user() -> None:
    global user_1_token
    message_details = {
        'user_name': 'Noa',
        'messages': ['Hi, how are you?'],
        'destination_name': USER2,
    }
    response = chat_client.post(
        "/send_message", json=message_details, params={'token': user_1_token}
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Unidentified user, not registered or not logged in"}


# -------------------------------------------- ____ get message tests ____ --------------------------------------------
# test receive message endpoint
def test_get_message():
    global user_2_token
    register_user2 = {"user_name": USER2, "user_password": USER2_PASSWORD}
    auth_client.post("/register", json=register_user2)

    login_user2 = {"user_name": USER2, "user_password": USER2_PASSWORD}
    response = auth_client.post("/login", json=login_user2)
    user_2_token = response.json()["user_token"]

    messages_response = chat_client.get(
        "/get_messages", params={'user_name': USER2, 'token': user_2_token}
    )
    assert messages_response.status_code == 200


# test receive message with invalid token
def test_get_message_with_invalid_token():
    messages_response = chat_client.get(
        "/get_messages", params={'user_name': USER2, 'token': 'aaaa'}
    )
    assert messages_response.status_code == 403
    assert messages_response.json() == {"detail": "Invalid or expired token."}


# test receive message with wrong user name
def test_get_message_with_wrong_user_name():
    global user_2_token
    messages_response = chat_client.get(
        "/get_messages", params={'user_name': "Noa", 'token': user_2_token}
    )
    assert messages_response.status_code == 404
    assert messages_response.json() == {
        "detail": "Unidentified user, not registered or not logged in"
    }
