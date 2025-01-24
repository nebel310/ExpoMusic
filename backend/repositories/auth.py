from database import new_session, UserOrm
from schemas import SUserRegister
from sqlalchemy import select
from passlib.context import CryptContext




pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserRepository:
    @classmethod
    async def register_user(cls, user_data: SUserRegister) -> int:
        async with new_session() as session:
            query = select(UserOrm).where(UserOrm.email == user_data.email)
            result = await session.execute(query)
            if result.scalars().first():
                raise ValueError("Пользователь с таким email уже существует")
            
            hashed_password = pwd_context.hash(user_data.password)
            
            user = UserOrm(
                username=user_data.username,
                email=user_data.email,
                hashed_password=hashed_password
            )
            session.add(user)
            await session.flush()
            await session.commit()
            return user.id
    
    @classmethod
    async def authenticate_user(cls, email: str, password: str) -> UserOrm | None:
        async with new_session() as session:
            query = select(UserOrm).where(UserOrm.email == email)
            result = await session.execute(query)
            user = result.scalars().first()
            
            if not user or not pwd_context.verify(password, user.hashed_password):
                return None
            
            return user
    
    @classmethod
    async def get_user_by_email(cls, email: str) -> UserOrm | None:
        async with new_session() as session:
            query = select(UserOrm).where(UserOrm.email == email)
            result = await session.execute(query)
            return result.scalars().first()