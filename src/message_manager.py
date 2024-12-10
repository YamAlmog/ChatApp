
import os
from typing import List, Dict
import hashlib
from errors import MessageManagerException
from datetime import datetime
from models import MessagesDetails
import psycopg2
from psycopg2.extras import execute_values

from dotenv import load_dotenv
load_dotenv()


class MessageManagerDB:
    def __init__(self) -> None:
        self.db_url = os.getenv("DATABASE_URL")

        # Corrected SQL query
        create_chat_messages_table = '''
            CREATE TABLE IF NOT EXISTS chat_messages(
                msg_id SERIAL PRIMARY KEY,
                user_src VARCHAR(255),
                user_dest VARCHAR(255),
                messages TEXT,
                time_stamp TIMESTAMP,
                is_delivered BOOL
            );
        '''

        try:
            # Establish connection and create the table
            with psycopg2.connect(self.db_url) as conn:
                with conn.cursor() as cursor:
                    cursor.execute(create_chat_messages_table)
                    print("===========>>>> Table created successfully")

        except psycopg2.Error as e:
            print(f"Error while creating the table: {e}")
        

        
    
    def insert_message_details(self, details:MessagesDetails, time_stamp:datetime) -> None:
        query = """
        INSERT INTO chat_messages (user_src, user_dest, messages, time_stamp, is_delivered)
        VALUES %s
        """
        # Prepare the values for bulk insertion
        values = [
            (details.user_name, details.destination_name, message, time_stamp, False)
            for message in details.messages
        ]

        try:
            with psycopg2.connect(self.db_url) as conn:
                with conn.cursor() as cursor:
                    # Bulk insert the parsed message details
                    execute_values(cursor, query, values)
                    conn.commit()
        except Exception as e:
            raise MessageManagerException(f"Failed to insert messages: {str(e)}")



    def filter_messages_for_user(self, user_name:str) -> List[Dict[str,str]]:
        query = "SELECT * FROM chat_messages WHERE user_dest = %s"
        try:
            with psycopg2.connect(self.db_url) as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query, (user_name,))
                    rows = cursor.fetchall()
                    print(rows)
                    print("=======================================")
                    messages = [{'from': row[1], 'message': row[3], 'at':row[4].strftime("%Y-%m-%d %H:%M:%S")} for row in rows]
                    print(messages)
                    return messages

        except Exception as e:
            raise MessageManagerException(f"{str(e)}")



    def retrieve_messages_of_given_user(self, user_name:str) -> List[Dict[str,str]]:
        try:
            messages = self.filter_messages_for_user(user_name)
            return messages
        except Exception as e:
            raise MessageManagerException(f"Failed to retrieve messages: {str(e)}")



