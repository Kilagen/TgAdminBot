import aiosqlite
from aiosqlite import Cursor

from typing import Dict, Any, Optional

from aiogram.fsm.storage.base import StorageKey, StateType
from aiogram.fsm.storage.memory import BaseStorage

from .setup import DATA_PATH, setup
from .base import UserStatus

class SqliteStorage(BaseStorage):
    def __init__(self):
        setup()

    async def set_state(self, key: StorageKey, state: StateType = None) -> None:
        pass

    async def get_state(self, key: StorageKey) -> Optional[str]:
        pass

    async def set_data(self, key: StorageKey, data: Dict[str, Any]) -> None:
        async with aiosqlite.connect(DATA_PATH) as conn:
            await conn.execute(
                "REPLACE INTO USERS (user_id, msg_cnt, status) "
                "VALUES (?, ?, ?)",
                (key.user_id, data["msg_cnt"], data["status"])
            )
            await conn.commit()

    async def get_data(self, key: StorageKey) -> Dict[str, Any]:
        async with aiosqlite.connect(DATA_PATH) as conn:
            cursor: Cursor = await conn.execute(
                "SELECT * FROM USERS "
                "WHERE user_id=?",
                (key.user_id, )
            )
            one = await cursor.fetchone()
            if one is None:
                return {"user_id": key.user_id, "msg_cnt": 0, "status": UserStatus.NOT_FOUND}
            return dict(one)

    async def close(self) -> None:
        pass