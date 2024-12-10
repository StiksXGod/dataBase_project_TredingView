from datetime import datetime
from typing import Optional
from pydantic import BaseModel
 
class User(BaseModel):
    id: int
    username: str
    refresh_token: Optional[str] = None  
    role: str
    created_at: datetime

    class Config:
        from_attributes = True

class RefreshTokenRequest(BaseModel):
    refresh_token: str

class UserName(BaseModel):
    username: str

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class CreateUserRequest(BaseModel):
    username: str
    password: str
    role: Optional[str] = "user"

class LoginUserRequest(BaseModel):
    username: str
    password: str
