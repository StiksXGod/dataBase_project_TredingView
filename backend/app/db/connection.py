import asyncpg
from core.config import DevelopmentConfig

async def get_db_pool() -> asyncpg.pool.Pool:
    pool = await asyncpg.create_pool(DevelopmentConfig.DATABASE_URL, min_size=DevelopmentConfig.MIN_SIZE_POOL, max_size=DevelopmentConfig.MAX_SIZE_POOL)
    return pool