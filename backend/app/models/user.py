from datetime import datetime
from typing import Optional
from pydantic import BaseModel
 
class User(BaseModel):
    id: int
    username: str
    refresh_token: Optional[str] = None  # Новое поле
    created_at: datetime

    class Config:
        from_attributes = True

class RefreshTokenRequest(BaseModel):
    refresh_token: str

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class CreateUserRequest(BaseModel):
    username: str
    password: str

class LoginUserRequest(BaseModel):
    username: str
    password: str
