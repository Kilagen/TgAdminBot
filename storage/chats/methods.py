import aiosqlite
from aiosqlite import Cursor
from storage.config import STORAGE_PATH
DATA_PATH = STORAGE_PATH / "data.sqlite"

def to_name(chat_id: int):
    return "chats.chat" + str(-chat_id)

async def create_chat_table(chat_id: int):
    async with aiosqlite.connect(DATA_PATH) as conn:
        await conn.execute(
            "CREATE TABLE IF NOT EXISTS %s ("
            "user_id INTEGER PRIMARY,"
            "msg_cnt INTEGER DEFAULT 0 NOT NULL"
            ")".format(to_name(chat_id))
        )
        await conn.commit()


async def check_if_table_exists(chat_id: int):
    async with aiosqlite.connect(DATA_PATH) as conn:
        cursor: Cursor = await conn.execute(
            "SELECT name FROM sqlite_master WHERE type = 'table' AND name = ?",
            (to_name(chat_id), )
        )
        table = await cursor.fetchone()
        return table is not None


async def get_message_count(chat_id: int, user_id: int) -> int:
    async with aiosqlite.connect(DATA_PATH) as conn:
        cursor: Cursor = await conn.execute(
            "SELECT msg_cnt FROM %s WHERE user_id = ?".format(to_name(chat_id)),
            (user_id, )
        )
        row = await cursor.fetchone()
        if row is None:
            return 0
        value = row[0]
        return value

async def increase_message_count(chat_id: int, user_id: int) -> None:
    async with aiosqlite.connect(DATA_PATH) as conn:
        if await get_message_count(chat_id, user_id) > 0:
            await conn.execute(
                "UPDATE %s "
                "SET msg_cnt = msg_cnt + 1 "
                "WHERE user_id = ?".format(to_name(chat_id)),
                (user_id, )
            )
        else:
            await conn.execute(
                "INSERT INTO %s(user_id, msg_cnt) "
                "VALUES (?, 1)".format(to_name(chat_id)),
                (user_id, )
            )
        await conn.commit()

if __name__ == "__main__":
    pass