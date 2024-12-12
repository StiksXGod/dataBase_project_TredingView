from typing import Optional
from api.auth import logger
from repositories.user import UserRepository
from fastapi import HTTPException, status
from utils.utils import hash_password,verify_password,decode_token,create_token
from core.config import DevelopmentConfig
from jose import jwt, JWTError, ExpiredSignatureError
from datetime import datetime
from models.user import AccessToken, DeleteUserId,User,UserName

async def get_user(repo: UserRepository, username: str) -> bool:
    user = await repo.check_username(username)
    if user:
        return True
    return False

async def user_delete(user_repo: UserRepository, username:UserName ,token:AccessToken) -> DeleteUserId:
    decode_token_user = await decode_token(token)
    if decode_token_user["user_role"]!="admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permission denaid")
    delete_user_id = await user_repo.delete_user_by_username(username.username)
    if not(delete_user_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found user") 
    return delete_user_id
    

async def login_auth(repo: UserRepository, username: str, password: str)-> Optional[User]:
    await username_password_checker(username, password)
    user = await repo.get_user_by_username(username)
    if not(user):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="No user with this username"
        )
    user_auth = await repo.get_user_auth(user.id)
    if user_auth:
        flag_passwd = verify_password(password,user_auth.password_hash)
        if flag_passwd:
            return user
        
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
    

async def verify_refresh_token(user_repo: UserRepository, refresh_token: str) -> list[str]:
    try:
        payload = await decode_token(refresh_token, token_type="refresh")
        username = payload.get("sub")
        user_id = payload.get("user_id")

        logger.info(f"id_user {user_id}")
        # logger.info(f"refresh_token {refresh_token}")

        if username is None or user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token payload",
                headers={"WWW-Authenticate": "Bearer"},
            )

        exp = payload.get("exp")
        current_time = datetime.utcnow().timestamp()

        if not exp or current_time > exp:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Refresh token has expired",
                headers={"WWW-Authenticate": "Bearer"},
            )

        is_valid = await user_repo.get_refresh_token(user_id)
        # logger.info(f"token {is_valid}")

        if not is_valid:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token",
                headers={"WWW-Authenticate": "Bearer"},
            )

        if is_valid.refresh_token != refresh_token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Wrong refresh token",
                headers={"WWW-Authenticate": "Bearer"},
            )

        user_data = await user_repo.get_user_by_id(user_id)

        new_access_token = await create_token(
            data={"sub": user_data.username, "user_id": user_data.id, "user_role": user_data.role},
            token_type="access"
        )

        time_remaining = exp - current_time
        logger.info(f"id_user {time_remaining}")
        refresh_token_threshold = 60 * 5  # 5 минут до истечения

        if time_remaining < refresh_token_threshold:
            new_refresh_token = await create_token(
                data={"sub": user_data.username, "user_id": user_data.id, "user_role": user_data.role},
                token_type="refresh"
            )
            await user_repo.update_refresh_token(user_id, new_refresh_token)
        else:
            new_refresh_token = refresh_token  # Оставляем старый refresh token

        return new_access_token, new_refresh_token

    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token: {e}",
            headers={"WWW-Authenticate": "Bearer"},
        )

async def role_cheacker(role:str)->None:
    if role != "admin" and role != "user":
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="role not supported rules")


async def create_user(repo: UserRepository, username: str, password:str, user_role:str)->int:
    await username_password_checker(username,password)
    await role_cheacker(role=user_role)
    hashed_password = await hash_password(password)
    id_created = await repo.create_user(username,user_role)
    await repo.set_user_auth(id_created,hashed_password)
    return id_created
