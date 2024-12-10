from utils.utils import create_token, decode_token
from datetime import datetime, timedelta
from logging import getLogger
from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from asyncpg.exceptions import UniqueViolationError
from db.connection import get_db_connection
from repositories.user import UserRepository
from services.auth import create_user, get_user, login_auth, verify_refresh_token
from models.user import CreateUserRequest, User, Token,RefreshTokenRequest

router = APIRouter()
logger = getLogger(__name__)

oauth_scheme = OAuth2PasswordBearer(tokenUrl = "/login")

@router.post("/register", tags=["Auth"], response_model=User)
async def register(user: CreateUserRequest, db=Depends(get_db_connection)):
    user_repo = UserRepository(db)
    try:
        if await get_user(user_repo, user.username):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User with this username already registered"
            )
        
        user_id = await create_user(user_repo, user.username, user.password)
        return {"id":user_id, "username":user.username, "refresh_token": None, "created_at": datetime.now()}
    
    except HTTPException as http_exc:
        raise http_exc
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Some problems with server - {e}"
        )


@router.post("/login", tags=["Auth"], response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db=Depends(get_db_connection)):
    user_repo = UserRepository(db)
    user_login = await login_auth(user_repo, form_data.username, form_data.password)
    if user_login:
        user_data = await user_repo.get_user_by_username(form_data.username)
        if not user_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        access_token = await create_token(
            data={"sub": user_data["username"], "user_id": user_data["id"]},
            token_type="access"
        )
        refresh_token = await create_token(
            data={"sub": user_data["username"], "user_id": user_data["id"]},
            token_type="refresh"
        )
        await user_repo.update_refresh_token(user_data["id"], refresh_token)
        logger.info(f"User {user_data["username"]} requested a new access token using refresh token.")
        return {"access_token": access_token, "refresh_token":refresh_token, "token_type": "bearer"}
    

@router.get("/id/{id}", tags=["Protected"], response_model=User)
async def get_user_info(
    id: int,
    token: str = Depends(oauth_scheme),
    db=Depends(get_db_connection)
):

    logger.info(f"Received token: {token}")
    user_data = await decode_token(token, token_type="access")
    logger.info(f"Decoded token data: {user_data}")
    token_username = user_data["sub"]  # Используем "sub" вместо "username"
    token_user_id = user_data["user_id"]

    if token_user_id != id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to access this resource"
        )

    user_repo = UserRepository(db)
    user = await user_repo.get_user_by_username(token_username)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return {
        "id": user["id"],
        "username": user["username"],
        "refresh_token": user["refresh_token"],
        "created_at": user["created_at"],
        "message": "User successfully authenticated and authorized."
    }

@router.post("/refresh", response_model=Token, tags=["Auth"])
async def refresh_token_endpoint(token_request: RefreshTokenRequest, db=Depends(get_db_connection)):
    user_repo = UserRepository(db)
    new_access_token, new_refresh_token = await verify_refresh_token(user_repo=user_repo ,refresh_token=token_request.refresh_token) # [access, refresh]

    return {
        "access_token": new_access_token,
        "refresh_token": new_refresh_token,
        "token_type": "bearer"
    }


@router.delete("/delete", tags=["delete"])
async def delete_user(user: User, db=Depends(get_db_connection)):
    repo = UserRepository(db)
    deleted = await repo.delete_user_by_username(user.username)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return {"message": f"User '{user.username}' deleted successfully"}