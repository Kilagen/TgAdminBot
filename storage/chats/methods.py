import aiosqlite
from aiosqlite import Cursor
from storage.config import STORAGE_PATH, DATA_PATH

def to_name(chat_id: int):
    return "chats.chat" + str(-chat_id)


async def _check_table_exists(chat_id: int, conn: aiosqlite.Connection) -> bool:
    cursor: Cursor = await conn.execute(
        "SELECT name FROM sqlite_master WHERE type = 'table' AND name = ?",
        (to_name(chat_id),)
    )
    table = await cursor.fetchone()
    return table is not None

async def _create_chat_table(chat_id: int, conn: aiosqlite.Connection) -> None:
    await conn.execute(
        "CREATE TABLE IF NOT EXISTS %s ("
        "user_id INTEGER PRIMARY,"
        "msg_cnt INTEGER DEFAULT 0 NOT NULL"
        ")".format(to_name(chat_id))
    )
    await conn.commit()

async def _get_message_count(chat_id: int, user_id: int, conn: aiosqlite.Connection) -> int:
    cursor: Cursor = await conn.execute(
        "SELECT msg_cnt FROM %s WHERE user_id = ?".format(to_name(chat_id)),
        (user_id,)
    )
    row = await cursor.fetchone()
    if row is None:
        return 0
    value = row[0]
    return value


async def _increment_message_count(chat_id: int, user_id: int, conn: aiosqlite.Connection) -> None:
    await conn.execute(
        "UPDATE %s "
        "SET msg_cnt = msg_cnt + 1 "
        "WHERE user_id = ?".format(to_name(chat_id)),
        (user_id,)
    )
    await conn.commit()


async def _add_message_count(chat_id: int, user_id: int, conn: aiosqlite.Connection) -> None:
    await conn.execute(
        "INSERT INTO %s(user_id, msg_cnt) "
        "VALUES (?, 1)".format(to_name(chat_id)),
        (user_id,)
    )
    await conn.commit()


async def table_exists(chat_id: int) -> bool:
    async with aiosqlite.connect(DATA_PATH) as conn:
        return await _check_table_exists(chat_id, conn)


async def create_chat_table(chat_id: int):
    async with aiosqlite.connect(DATA_PATH) as conn:
        if not await _check_table_exists(chat_id, conn):
            await _create_chat_table(chat_id, conn)


async def get_message_count(chat_id: int, user_id: int) -> int:
    async with aiosqlite.connect(DATA_PATH) as conn:
        if not await _check_table_exists(chat_id, conn):
            await _create_chat_table(chat_id, conn)
            return 0
        return await _get_message_count(chat_id, user_id, conn)


async def increase_message_count(chat_id: int, user_id: int) -> None:
    async with aiosqlite.connect(DATA_PATH) as conn:
        if not await _check_table_exists(chat_id, conn):
            await _create_chat_table(chat_id, conn)
            await _add_message_count(chat_id, user_id, conn)
            return None

        if await _get_message_count(chat_id, user_id, conn) > 0:
            await _increment_message_count(chat_id, user_id, conn)
        else:
            await _add_message_count(chat_id, user_id, conn)


if __name__ == "__main__":
    pass
