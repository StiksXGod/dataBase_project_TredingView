from passlib.context import CryptContext
from datetime import datetime, timedelta
from fastapi import status, HTTPException
from jose import JWTError, jwt
from core.config import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, SECRET_KEY_ACCESS, SECRET_KEY_REFRESH, REFRESH_TOKEN_EXPIRE_DAYS

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def decode_token(token: str, token_type: str = "access"):
    """
    Расшифровывает токен в зависимости от его типа (access/refresh).
    """
    secret_key = (
        SECRET_KEY_ACCESS if token_type == "access" else SECRET_KEY_REFRESH
    )
    
    try:
        payload = jwt.decode(token, secret_key, algorithms=[ALGORITHM])
        return payload  
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid or expired {token_type} token",
            headers={"WWW-Authenticate": "Bearer"},
        )

async def create_token(data: dict, token_type: str):
    to_encode = data.copy()
    if token_type == "access":
        expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        SECRET_KEY = SECRET_KEY_ACCESS
    elif token_type == "refresh":
        expire = datetime.now() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
        SECRET_KEY = SECRET_KEY_REFRESH
    else:
        raise ValueError("Invalid token type")
    to_encode.update({"exp": expire, "type": token_type})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def hash_password(password: str)-> str:
    return pwd_context.hash(password)

async def verify_password(plain_password: str,hashed_password:str)->bool:
    return pwd_context.verify(plain_password,hashed_password)