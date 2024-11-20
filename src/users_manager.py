import psycopg2
from psycopg2 import sql
from psycopg2.extras import execute_values
from typing import Optional
from errors import InvalidUserName, InvalidPassword, InvalidToken, UnregisteredUser, UsersManagerException
import re
import hashlib
import datetime
import os
from typing import Dict

MIN_PASSWOED_LEN = 5 



class UserManagerDB:
    def __init__(self) -> None:
        self.db_url = os.getenv("DATABASE_URL")

        CREATE_REGISTERED_TABLE_QUERY = """
            CREATE TABLE IF NOT EXISTS registered_users (
                user_name VARCHAR(50) PRIMARY KEY,
                user_password VARCHAR(128) NOT NULL,
            );
            """
        CREATE_LOGIN_TABLE_QUERY = """
            CREATE TABLE IF NOT EXISTS login_users (
                user_name VARCHAR(50) PRIMARY KEY,
                user_token VARCHAR(128) NOT NULL,
            );
            """
        try:
            # Establish connection and create the table
            with psycopg2.connect(self.db_url) as conn:
                with conn.cursor() as cursor:
                    cursor.execute(CREATE_REGISTERED_TABLE_QUERY)
                    print("===========>>>> registered_users table created successfully")
                    cursor.execute(CREATE_LOGIN_TABLE_QUERY)
                    print("===========>>>> login_users table created successfully")

        except psycopg2.Error as e:
            print(f"Error while creating the table: {e}")
        


    def is_exist_user(self, user_name:str) -> bool:
        query = f"SELECT 1 FROM registered_users WHERE user_name = {user_name}"
        try:
            with psycopg2.connect(self.db_url) as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query)
                    # Fetch one result
                    result = cursor.fetchone()
                    # Close the connection
                    conn.close()
                
            # Return True if a result is found, otherwise False
            return result is not None
        except Exception as e:
            raise UsersManagerException(e)

    
    def register_user(self, user_name:str,  :str) -> str:
        query = """
        INSERT INTO registered_users (user_name, user_password)
        VALUES %s
        """
        try:
            if not self.is_exist_user(user_name):
                hash_password = AuthenticationHandler.hash_element(user_password)
                values = [user_name, hash_password]
                with psycopg2.connect(self.db_url) as conn:
                    with conn.cursor() as cursor:
                        execute_values(cursor, query, values)
                        conn.commit()
                return "User successfully registered"
            else:
                raise InvalidUserName("This username is already in use, please choose another name.")
            
        except Exception as e:
            raise UsersManagerException(f"Failed to insert user details: {str(e)}")
        

    def insert_name_and_token(self, name:str, token:str) -> None:
        try:   
            # if user name exist in login only update the token 
            query = """
            INSERT INTO login_users (user_name, user_token)
            VALUES (%s, %s)
            ON CONFLICT (user_name)
            DO UPDATE SET user_token = EXCLUDED.user_token
            """
            with psycopg2.connect(self.db_url) as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query,(name, token))
                    conn.commit()
        except Exception as e:
            raise UsersManagerException(f"Failed to insert user token into login_users: {str(e)}")


    def login_user(self, user_name:str, password:str) -> str:
        try:
            if not self.is_exist_user(user_name):
                raise UnregisteredUser("Unregistered user, Please sign up")
            elif AuthenticationHandler.is_valid_password(user_name, password, self.db_url):
                current_time = str(datetime.datetime.now())
                token = AuthenticationHandler.hash_element(f"{user_name}{password}{current_time}")
                self.insert_name_and_token(user_name, token)
                return token
            else:
                raise InvalidPassword(f"Error: {e}")
        except Exception as e:
            raise Exception(e)




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
    def is_valid_password(user_name:str, user_password:str, url: str):
        hash_password = AuthenticationHandler.hash_element(user_password)
        
        query = "SELECT 1 FROM registered_users WHERE user_name = ? AND user_password = ?"
        with psycopg2.connect(url) as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, (user_name, hash_password))
                result = cursor.fetchone()
                conn.commit()
                # Check if a result was found
                if result:
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
    # try:    
    #     user_manager = UserManager()
    #     print(user_manager.register_dict)
    #     user_manager.register_user('Yam', '15a234')
    #     print(user_manager.register_dict)
    #     auth_hendler = AuthenticationHandler()
    #     # print(auth_hendler.is_valid_password('Yam', '15a234', user_manager.register_dict))

    #     usr_token = user_manager.login_user("Yam", '15a234')
    #     print(usr_token)
    #     loging_dict = user_manager.loging_dict
    #     print(loging_dict)

    #     is_valid_token = auth_hendler.is_valid_token(usr_token, '15a234', loging_dict)
    #     print("Token is: ",is_valid_token)

    # except Exception as e:
    #     print(str(e))
    pass
if __name__ == '__main__':
    main()