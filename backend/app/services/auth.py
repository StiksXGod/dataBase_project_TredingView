from typing import List
from api.auth import logger
from passlib.context import CryptContext
from repositories.user import UserRepository
from fastapi import HTTPException, status
from utils.utils import hash_password,verify_password,decode_token,create_token
from core.config import DevelopmentConfig

async def get_user(repo: UserRepository, username: str) -> bool:
    user = await repo.check_username(username)
    if user:
        return True
    return False

async def login_auth(repo: UserRepository, username: str, password: str)->bool:
    await username_password_checker(username, password)
    user = await get_user(repo, username)
    if not(user):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="no user with this username"
        )
    auth_user = await authenticate_user(repo,username,password)
    if auth_user:
        return True
    raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="uncorrect password or username"
        )

async def username_password_checker(username:str, password:str)->None:
    flag_usrn = all(char in DevelopmentConfig.ALLOWED_CHARACTERS for char in username)
    flag_passwd = all(char in DevelopmentConfig.ALLOWED_CHARACTERS for char in password)
    if len(username)>18 or len(username)<5 or not(flag_usrn):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="username not supported rules")
    if len(password)>22 or len(password)<8 or not(flag_passwd):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="password not supported rules")
    

async def verify_refresh_token(user_repo: UserRepository, refresh_token:str)->List[str]:
    payload = await decode_token(refresh_token, token_type="refresh")
    username = payload.get("sub")
    user_id = payload.get("user_id")
    logger.info(f"id_user {user_id}")
    if username is None or user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
            headers={"WWW-Authenticate": "Bearer"},
        )

    is_valid = await user_repo.verify_refresh_token(user_id)
    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if is_valid!=refresh_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="wrong refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    
    new_access_token = await create_token(
        data={"sub": username, "user_id": user_id},
        token_type="access"
    )

    new_refresh_token = await create_token(
        data={"sub": username, "user_id": user_id},
        token_type="refresh"
    )
    
    await user_repo.update_refresh_token(user_id, new_refresh_token)
    return new_access_token, new_refresh_token

async def role_cheacker(role:str)->None:
    if role != "admin" and role != "user":
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="role not supported rules")


async def create_user(repo: UserRepository, username: str, password:str, user_role:str)->int:
    await username_password_checker(username,password)
    await role_cheacker(role=user_role)
    hashed_password = await hash_password(password)
    return await repo.create_user(username,hashed_password,user_role)

async def authenticate_user(repo: UserRepository, username: str, password: str)->bool:
    user = await repo.get_user_by_username(username)
    if user and await verify_password(password, user["password_hash"]):
        return True
    return False  

async def delete_user(repo: UserRepository, username: str)->bool:
    return await repo.delete_user_by_username(username)