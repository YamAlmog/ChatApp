import os
import psycopg2


class ChatDBManager:
    def __init__(self) -> None:
        self.db_url = os.getenv("DATABASE_URL")

        create_chat_db_table = '''
            CREATE TABLE IF NOT EXIST chat_db(
            msg_id VARCHAR(255) PRIMARY KEY,
            user_src VARCHAR,
            user_dst VARCHAR,
            msg TEXT,
            time_stamp DATETIME);'''
    
    def insert_massage_details() -> None:
        pass