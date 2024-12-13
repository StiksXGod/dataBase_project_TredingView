from asyncpg import Connection
from typing import Optional
from asyncpg import Connection
from datetime import datetime
from core.logger import logger
from models.user import User,UserAuth,RefreshTokenRequest

class UserRepository:
    
    def __init__(self,connection: Connection):
        self.connection = connection
    
    async def create_user(self, username: str, role: str) -> int:
        query = """
            INSERT INTO users (username, role,created_at)
            VALUES ($1, $2, $3)
            RETURNING id
        """
        created_at = datetime.utcnow()
        record = await self.connection.fetchrow(query, username, role, created_at)
        return record['id']
    
    async def check_username(self, username: str) -> str:
        query = """
        SELECT username
        FROM Users
        WHERE username = $1;
        """
        result = await self.connection.fetchval(query, username)
        return result
    
    async def get_user_by_username(self, username: str) -> Optional[User]:
        query = "SELECT id, username, role, created_at FROM users WHERE username = $1"
        record = await self.connection.fetchrow(query, username)
        if record:
            return User(**record)
        return None
    
    async def get_user_by_id(self, user_id: int) -> Optional[User]:
        query = "SELECT id, username, role, created_at FROM users WHERE id = $1"
        record = await self.connection.fetchrow(query, user_id)
        if record:
            return User(**record)
        return None


    async def delete_user_by_username(self, username: str) -> Optional[int]:
        find_query = "SELECT id FROM users WHERE username = $1"
        user = await self.connection.fetchrow(find_query, username)
        
        if not user:
            return None  # Пользователь не найден

        user_id = user["id"]

        delete_query = "DELETE FROM users WHERE username = $1"
        result = await self.connection.execute(delete_query, username)
        
        if result == "DELETE 1":
            return user_id  # Успешно удалён, возвращаем ID
        return None
    
    async def set_user_auth(self, user_id: int, password: str, refresh_token: Optional[str] = None):
        query = """
            INSERT INTO user_auth (user_id, password_hash, refresh_token)
            VALUES ($1, $2, $3)
            ON CONFLICT (user_id) DO UPDATE SET password_hash = EXCLUDED.password_hash, refresh_token = EXCLUDED.refresh_token
        """
        await self.connection.execute(query, user_id, password, refresh_token)

    async def get_user_auth(self, user_id: int) -> Optional[UserAuth]:
        query = "SELECT user_id, password_hash, refresh_token, last_login FROM user_auth WHERE user_id = $1"
        record = await self.connection.fetchrow(query, user_id)
        if record:
            return UserAuth(**record)
        return None
    
    async def update_refresh_token(self, user_id: int, refresh_token: str):
        query = "UPDATE user_auth SET refresh_token = $1, last_login = CURRENT_TIMESTAMP WHERE user_id = $2"
        await self.connection.execute(query, refresh_token, user_id)

    async def get_user_by_refresh_token(self, refresh_token: str) -> Optional[UserAuth]:
        query = "SELECT user_id, password_hash, refresh_token, last_login FROM user_auth WHERE refresh_token = $1"
        record = await self.connection.fetchrow(query, refresh_token)
        if record:
            return UserAuth(**record)
        return None
    
    async def get_refresh_token(self, user_id: int) -> Optional[RefreshTokenRequest]:
        query = "SELECT refresh_token FROM user_auth WHERE user_id = $1"
        stored_refresh_token = await self.connection.fetchrow(query, user_id)
        
        if stored_refresh_token and "refresh_token" in stored_refresh_token:
            refresh_token_value = stored_refresh_token["refresh_token"]
            return RefreshTokenRequest(refresh_token=refresh_token_value)
        
        return None
