import asyncio
import typing as tp


async def delay(coro, delay: float) -> None:
    await asyncio.sleep(delay)
    await coro
