from utils.utils import create_token, decode_token
from datetime import datetime, timedelta
from core.logger import logger
from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from asyncpg.exceptions import UniqueViolationError
from dependencies.dependencies import get_db_connection
from repositories.user import UserRepository
from services.auth import create_user, get_user, login_auth, verify_refresh_token, user_delete
from models.user import CreateUserRequest, User, Token,RefreshTokenRequest, UserName, CreatedUserResponse, DeleteUserId, UserLoginResponse

router = APIRouter()

oauth_scheme = OAuth2PasswordBearer(tokenUrl = "/login")

@router.post("/register", tags=["Auth"], response_model=CreatedUserResponse)
async def register(user: CreateUserRequest, db=Depends(get_db_connection)):
    user_repo = UserRepository(db)
    try:
        if await get_user(user_repo, user.username):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User with this username already registered"
            )
        user_id = await create_user(user_repo, user.username, user.password, user_role=user.role)
        return {"id": user_id, "message": "User created successfully."}
    
    except HTTPException as http_exc:
        raise http_exc
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Some problems with server - {e}"
        )


@router.post("/login", tags=["Auth"], response_model=UserLoginResponse)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db=Depends(get_db_connection)):
    user_repo = UserRepository(db)
    try:
        user_data = await login_auth(user_repo, form_data.username, form_data.password)
        access_token = await create_token(
            data={"sub": user_data.username, "user_id": user_data.id, "user_role":user_data.role},
            token_type="access"
        )
        refresh_token = await create_token(
            data={"sub": user_data.username, "user_id": user_data.id, "user_role":user_data.role},
            token_type="refresh"
        )
        await user_repo.update_refresh_token(user_data.id, refresh_token)
        logger.info(f"User {user_data.username} requested a new access token using refresh token.")
        return {"access_token": access_token, "user_id": user_data.id}
    except HTTPException as http_exc:
        raise http_exc
    

@router.get("/id/{id}", tags=["Protected"], response_model=User)
async def get_user_info(
    id: int,
    token: str = Depends(oauth_scheme),
    db=Depends(get_db_connection)
):
    try:
        logger.info(f"Received token: {token}")
        user_data = await decode_token(token, token_type="access")
        logger.info(f"Decoded token data: {user_data}")
        token_username = user_data["sub"]  # Используем "sub" вместо "username"
        token_user_id = user_data["user_id"]
        logger.info(f"Current time: {datetime.utcnow().timestamp()}")


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
            "id": user.id,
            "username": user.username,
            "created_at": datetime.fromisoformat(str(user.created_at)).strftime("%Y-%m-%d %H:%M:%S")
,
            "role": user.role,
            "message": "User successfully authenticated and authorized."
        }
    except HTTPException as http_exc:
        raise http_exc
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Some problems with server - {e}"
        )


@router.post("/refresh", response_model=Token, tags=["Auth"])
async def refresh_token_endpoint(token_request: RefreshTokenRequest, db=Depends(get_db_connection)):
    user_repo = UserRepository(db)
    new_access_token, new_refresh_token = await verify_refresh_token(user_repo=user_repo ,refresh_token=token_request.refresh_token) # [access, refresh]
    logger.info(f"Decoded token data: {new_refresh_token}")

    return {
        "access_token": new_access_token,
        "refresh_token": new_refresh_token,
        "token_type": "bearer"
    }


@router.delete("/delete",tags=["Protected"], response_model=DeleteUserId)
async def delete_user(
    username: UserName,
    token: str = Depends(oauth_scheme),
    db=Depends(get_db_connection)
):
    repo = UserRepository(db)
    try:
        delete_user_id = await user_delete(repo,username,token)
        return DeleteUserId(id=delete_user_id)
    
    except HTTPException as http:
        raise http
    
    except Exception as e:
        raise e