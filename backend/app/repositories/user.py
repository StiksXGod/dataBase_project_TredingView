from typing import Union
from asyncpg import Connection
from datetime import datetime

class UserRepository:
    def __init__(self,db:Connection):
        self.db = db
    
    async def create_user(self, username:str, password_hash:str)->int:
        query = """
        INSERT INTO Users (username, password_hash, created_at)
        VALUES ($1, $2, $3)
        RETURNING id;
        """
        created_at = datetime.now()
        return await self.db.fetchval(query, username, password_hash, created_at)
    
    async def check_username(self, username: str) -> str:
        query = """
        SELECT username
        FROM Users
        WHERE username = $1;
        """
        result = await self.db.fetchval(query, username)
        return result

    async def delete_user_by_username(self, username: str) -> bool:
        query = "DELETE FROM Users WHERE username = $1;"
        result = await self.db.execute(query, username)
        deleted_count = int(result.split(" ")[1])
        return deleted_count > 0
    
    async def get_user_by_username(self, username: str) ->str:
        """Получение пользователя по имени пользователя"""
        query = """
        SELECT id, username, password_hash, refresh_token, created_at
        FROM Users
        WHERE username = $1
        """
        return await self.db.fetchrow(query, username)
    
    async def update_refresh_token(self, user_id: int, refresh_token: str):
        query = "UPDATE Users SET refresh_token = $1 WHERE id = $2"
        await self.db.execute(query, refresh_token, user_id)
    
    async def get_refresh_token(self, refresh_token:str, user_id: int):
        query = "UPDATE Users SET refresh_token = $1 WHERE id = $2"
        await self.db.execute(query, refresh_token, user_id)

    async def verify_refresh_token(self, user_id: int, refresh_token: str) -> bool:
        query = "SELECT refresh_token FROM Users WHERE id = $1"
        stored_refresh_token = await self.db.fetchval(query, user_id)
        return stored_refresh_token
