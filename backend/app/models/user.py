from datetime import datetime
from typing import Optional
from pydantic import BaseModel
 
class UserAuth(BaseModel):
    password_hash :str
    refresh_token: Optional[str] = None
    last_login: Optional[datetime] = None 

class CreatedUserResponse(BaseModel):
    id:int

class UserId(BaseModel):
    id:int
 
class User(BaseModel):
    id: int
    username: str
    role: str
    created_at: datetime

    class Config:
        from_attributes = True

class RefreshTokenRequest(BaseModel):
    refresh_token: str

class AccessToken(BaseModel):
    token : str

class UserName(BaseModel):
    username: str

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
class UserLoginResponse(BaseModel):
    access_token: str
    user_id: int

class CreateUserRequest(BaseModel):
    username: str
    password: str
    role: Optional[str] = "user"
 
class DeleteUserId(BaseModel):
    id:int