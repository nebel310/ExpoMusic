from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from database import new_session, BlacklistedTokenOrm, UserOrm
from sqlalchemy import select, delete
from repositories.auth import UserRepository




SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme)) -> UserOrm:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Не удалось подтвердить учетные данные",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    async with new_session() as session:
        query = delete(BlacklistedTokenOrm).where(BlacklistedTokenOrm.expires_at < datetime.now(timezone.utc))
        await session.execute(query)
        await session.commit()
    
    async with new_session() as session:
        query = select(BlacklistedTokenOrm).where(BlacklistedTokenOrm.token == token)
        result = await session.execute(query)
        if result.scalars().first():
            raise credentials_exception
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = await UserRepository.get_user_by_email(email)
    if user is None:
        raise credentials_exception
    
    return user