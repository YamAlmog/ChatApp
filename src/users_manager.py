# import psycopg2
# from psycopg2 import sql
# from psycopg2.extras import execute_values
from typing import Optional
from errors import InvalidUserName, InvalidPassword, InvalidToken, UnregisteredUser
import re
import hashlib
import datetime

MIN_PASSWOED_LEN = 5 

# # Database Configuration
# DB_CONFIG = {
#     'dbname': 'ChatDB',
#     'user': 'postgres',
#     'password': '123456',
#     'host': 'localhost',
#     'port': 5432
# }

# # SQL Queries
# CREATE_TABLE_QUERY = """
# CREATE TABLE IF NOT EXISTS users (
#     id SERIAL PRIMARY KEY,
#     user_name VARCHAR(50) NOT NULL UNIQUE,
#     user_password VARCHAR(128) NOT NULL,
#     token VARCHAR(256)
# );
# """

# class UsersDataset:
#     def __init__(self, config):
#         self.conn = psycopg2.connect(**config)
#         self.cursor = self.conn.cursor()

    
#     def create_table(self):
#         self.cursor.execute(CREATE_TABLE_QUERY)
#         self.conn.commit()



class UserManager:
    def __init__(self) -> None:
        self.register_dict = {}
        self.loging_dict = {}


    def register_user(self, user_name:str, user_password:str) -> None:
        try:
            if AuthenticationHandler.verified_password(user_password):
                if user_name not in self.register_dict.keys():
                    self.register_dict[user_name] = AuthenticationHandler.hash_element(user_password)
                else:
                    raise InvalidUserName("This username is already in use, please choose another name.")
        except InvalidPassword as e:
            raise InvalidPassword(f"Error: {e}")


    def login_user(self, user_name:str, password:str) -> str:
        try:
            if user_name not in self.register_dict.keys():
                raise UnregisteredUser("Unregistered user, Please sign up")
           
            elif AuthenticationHandler.is_valid_password(user_name, password, self.register_dict):
                current_time = str(datetime.datetime.now())
                token = AuthenticationHandler.hash_element(user_name+password+current_time)
                hash_pass = AuthenticationHandler.hash_element(password)
                self.loging_dict[hash_pass] = token
                return token
        except InvalidPassword as e:
            raise InvalidPassword(f"Error: {e}")


class AuthenticationHandler:
    @staticmethod
    def verified_password(password:str) -> Optional[bool]:
        # check password conventions like len, letters, numbers
        # return exception if not valid and the password ruls
        if len(password) < MIN_PASSWOED_LEN:
            raise InvalidPassword(f"Password length must be longer then {MIN_PASSWOED_LEN}")
        if not re.search("[a-zA-Z]", password):
            raise InvalidPassword("Password must contain at least one letter")
        else:
            return True


    @staticmethod
    def hash_element(element:str) -> str:
        return hashlib.sha256(element.encode()).hexdigest()
    

    @staticmethod
    def is_valid_password(user_name:str, user_password:str, user_dict: dict):
        hash_password = AuthenticationHandler.hash_element(user_password)
        if user_dict[user_name] == hash_password:
            return True
        else:
            raise InvalidPassword("Wrong Password")
    

    @staticmethod
    def is_valid_token(token:str, password:str, login_dict:dict) -> bool:
        hash_password = AuthenticationHandler.hash_element(password)
        if login_dict[hash_password] == token:
            return True
        else:
            raise InvalidToken("Wrong Token")



# POC:
def main():
    # user_ds = UsersDataset(DB_CONFIG)
    # user_ds.create_table()
    try:    
        user_manager = UserManager()
        print(user_manager.register_dict)
        user_manager.register_user('Yam', '15a234')
        print(user_manager.register_dict)
        auth_hendler = AuthenticationHandler()
        # print(auth_hendler.is_valid_password('Yam', '15a234', user_manager.register_dict))

        usr_token = user_manager.login_user("Yam", '15a234')
        print(usr_token)
        loging_dict = user_manager.loging_dict
        print(loging_dict)

        is_valid_token = auth_hendler.is_valid_token(usr_token, '15a234', loging_dict)
        print("Token is: ",is_valid_token)

    except Exception as e:
        print(str(e))
if __name__ == '__main__':
    main()