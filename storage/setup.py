import os
import sqlite3

from .config import STORAGE_PATH, DATA_PATH

def create_user_data_table() -> None:
    with sqlite3.connect(DATA_PATH) as conn:
        conn.execute(
            "CREATE TABLE IF NOT EXISTS USERS ("
            "user_id INTEGER PRIMARY KEY,"
            "msg_cnt INTEGER DEFAULT 0 NOT NULL,"
            "status INTEGER DEFAULT -1"
            ")"
        )
        conn.commit()

def create_bad_messages_table() -> None:
    with sqlite3.connect(DATA_PATH) as conn:
        conn.execute(
            "CREATE TABLE IF NOT EXISTS BAD_MESSAGES ("
            "user_id INTEGER NOT NULL,"
            "msg_id INTEGER NOT NULL"
            ")"
        )
        conn.commit()


def setup():
    os.makedirs(STORAGE_PATH, exist_ok=True)
    DATA_PATH.touch(exist_ok=True)
    create_user_data_table()
    create_bad_messages_table()

