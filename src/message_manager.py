# import psycopg2
import os
from typing import List
import hashlib
from errors import messageManagerException
import datetime
from models import ReceiveMessage

from dotenv import load_dotenv
load_dotenv()


# class messageManager:
#     def __init__(self) -> None:
#         # self.db_url = os.getenv("DB_URL")

#         create_chat_db_table = '''
#             CREATE TABLE IF NOT EXIST chat_db(
#             msg_id VARCHAR(255) PRIMARY KEY,
#             user_src VARCHAR,
#             user_dst VARCHAR,
#             msg TEXT,
#             time_stamp DATETIME);'''
        
  
#         with psycopg2.connect(database="ChatDB",
#         user="postgres",
#         password="123456",
#         host="localhost",
#         port="5432") as conn:
#             cursor = conn.cursor()
#             cursor.execute(create_chat_db_table)
    
#     def insert_message_details() -> None:
#         pass


class messageManager:
    def __init__(self) -> None:
        self.messages_dict= {}


    def insert_message_details(self, user_src: str, user_dst: str, msg: List[str], time_stamp: str) -> None: 
        try:
            value = {'user_src': user_src.lower(),
                    'user_dst': user_dst.lower(),
                    'message': msg,
                    'time': time_stamp}
            msg_as_string = ''.join(msg)
            concat_value = user_src+user_dst+msg_as_string+time_stamp
            msg_hash = hashlib.sha256(concat_value.encode()).hexdigest()
            self.messages_dict[msg_hash] = value
        except Exception as e:
            raise messageManagerException(f'message insertion fails: {e}')
        


    def filter_messages_for_user(self, user_name:str) -> dict:
        filtered_dict = [value for value in self.messages_dict.values() if value.get('user_dst') == user_name.lower()]
        return filtered_dict



    def arrange_message_to_sent(self, user_name:str) -> List[ReceiveMessage]:
        list_of_messages_to_user = self.filter_messages_for_user(user_name.lower())
        tuple_of_usr_and_msg = [(item['user_src'], item['message']) for item in list_of_messages_to_user]
        result = []
        for usr_name, msg in tuple_of_usr_and_msg:
            return_format = ReceiveMessage(From = usr_name, message = msg)
            result.append(return_format.model_dump())

        return result




# POC
def main() -> None:
    msg_manager = messageManager()
    src_name = 'Yam'
    dst_name = 'Roi'
    msg = ['hello']
    time = str(datetime.datetime.now())
    msg_manager.insert_message_details(src_name, dst_name, msg, time)

    src_name1 = 'Yam'
    dst_name1 = 'Roi'
    msg1 = ['hi']
    time1 = str(datetime.datetime.now())
    msg_manager.insert_message_details(src_name1, dst_name1, msg1, time1)

    list_of_messages_to_roi = msg_manager.filter_messages_for_user("Roi")
    print(list_of_messages_to_roi)
    print(type(list_of_messages_to_roi))
    print(msg_manager.arrange_message_to_sent('roi'))
if __name__ == "__main__":
    main()