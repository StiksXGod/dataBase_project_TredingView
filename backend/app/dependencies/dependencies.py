from fastapi import Depends, Request
import asyncpg
from typing import AsyncGenerator


async def get_db_connection(request: Request) -> AsyncGenerator[asyncpg.Connection, None]:
    pool: asyncpg.pool.Pool = request.app.state.pool
    async with pool.acquire() as connection:
        yield connection