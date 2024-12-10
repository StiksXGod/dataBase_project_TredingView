import asyncpg
from fastapi import Depends
from core.config import DATABASE_URL


async def get_db_connection():
    conn = await asyncpg.connect(DATABASE_URL)
    try:
        yield conn
    finally:
        await conn.close()
