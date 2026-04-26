from datetime import datetime, timedelta
from typing import Optional

from jose import JWTError, jwt
from passlib.context import CryptContext
from app.core.config import settings


# it defines the password crypting algorithim
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# this function hash the password
def hash_password(password: str) -> str:
    password_bytes = password.encode("utf-8")[:72]  # truncate BYTES
    return pwd_context.hash(password_bytes)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    password_bytes = plain_password.encode("utf-8")[:72]
    return pwd_context.verify(password_bytes, hashed_password)

# now after hasing we need to create the jwt token
def create_access_token(data : dict,  expires_delta: Optional[timedelta] = None)-> str:
    to_encode = data.copy()
    expire = datetime.utcnow()+(
        expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def decode_token(token: str) -> Optional[dict]:
    
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        return payload
    except JWTError:
        return None