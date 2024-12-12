import asyncpg
from fastapi import Depends
from core.config import DevelopmentConfig


async def get_db_connection():
    conn = await asyncpg.connect(DevelopmentConfig.DATABASE_URL)
    try:
        yield conn
    finally:
        await conn.close()
