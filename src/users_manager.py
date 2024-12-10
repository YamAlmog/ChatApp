import psycopg2
from typing import Optional
from errors import InvalidUserName, InvalidPassword, UserNotFoundError, UnregisteredUser, UsersManagerException
import re
import hashlib
import datetime
import os
from typing import Dict

MIN_PASSWOED_LEN = 5 



class UserManagerDB:
    def __init__(self) -> None:
        self.db_url = os.getenv("DATABASE_URL")

        CREATE_REGISTERED_TABLE_QUERY = '''
            CREATE TABLE IF NOT EXISTS registered_users(
                user_name VARCHAR(50) PRIMARY KEY,
                user_password VARCHAR(128) NOT NULL
            );
            '''
        CREATE_LOGIN_TABLE_QUERY = '''
            CREATE TABLE IF NOT EXISTS login_users(
                user_name VARCHAR(50) PRIMARY KEY,
                user_token VARCHAR(128) NOT NULL
            );
            '''
        try:
            # Establish connection and create the table
            with psycopg2.connect(self.db_url) as conn:
                with conn.cursor() as cursor:
                    cursor.execute(CREATE_REGISTERED_TABLE_QUERY)
                    print("===========>>>> registered_users table created successfully")
                    cursor.execute(CREATE_LOGIN_TABLE_QUERY)
                    print("===========>>>> login_users table created successfully")

        except psycopg2.Error as e:
            print(f"Error while creating table: {e}")
        



    def is_exist_user(self, user_name:str) -> bool:
        query = "SELECT 1 FROM registered_users WHERE user_name = %s"
        try:
            with psycopg2.connect(self.db_url) as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query, (user_name,))
                    # Fetch one result
                    result = cursor.fetchone()
                
            # Return True if a result is found, otherwise False
            return result is not None
        except Exception as e:
            raise UsersManagerException(e)

    
    def register_user(self, user_name:str,  user_password:str) -> str:
        query = """
        INSERT INTO registered_users (user_name, user_password)
        VALUES (%s ,%s)
        """
        try:
            if self.is_exist_user(user_name) == False:
                hash_password = AuthenticationHandler.hash_element(user_password)
                with psycopg2.connect(self.db_url) as conn:
                    with conn.cursor() as cursor:
                        cursor.execute(query, (user_name, hash_password))
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
                raise UnregisteredUser("Unregistered user, Please sign up first")
            elif AuthenticationHandler.is_valid_password(user_name, password, self.db_url):
                current_time = str(datetime.datetime.now())
                token = AuthenticationHandler.hash_element(f"{user_name}{password}{current_time}")
                self.insert_name_and_token(user_name, token)
                return token
            else:
                raise InvalidPassword("You entered an incorrect password")
        except InvalidPassword:
            raise    
        except Exception as e:
            raise Exception(f"Error: {e}")


        
    def authenticate_token(self, token:str, user_name:str) -> bool:
        try:
            query = "select user_token from login_users where user_name = %s"
            with psycopg2.connect(self.db_url) as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query, (user_name, ))
                    result = cursor.fetchone()
                    
                    if not result:
                        raise UserNotFoundError(f"User {user_name} not found")
                    
                    # Check if a result was found
                    return result[0] == token
                        
        except UserNotFoundError:
            raise            
        except Exception as e:
            raise Exception(f"Error: {e}")




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
    def is_valid_password(user_name:str, user_password:str, url: str) -> bool:
        hash_password = AuthenticationHandler.hash_element(user_password)
        
        query = "SELECT 1 FROM registered_users WHERE user_name = %s AND user_password = %s"
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


    
