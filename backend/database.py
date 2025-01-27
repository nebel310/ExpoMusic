from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import ForeignKey, DateTime, delete, select




engine = create_async_engine(
    "postgresql+asyncpg://postgres:123456@localhost/expomusic_db"
)

new_session = async_sessionmaker(engine, expire_on_commit=False)

class Model(DeclarativeBase):
    pass


class UserOrm(Model):
    __tablename__ = 'users'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    hashed_password: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    is_active: Mapped[bool] = mapped_column(default=True)


class RefreshTokenOrm(Model):
    __tablename__ = 'refresh_tokens'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    token: Mapped[str] = mapped_column(unique=True)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


class BlacklistedTokenOrm(Model):
    __tablename__ = 'blacklisted_tokens'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    token: Mapped[str] = mapped_column(unique=True)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.create_all)

async def delete_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.drop_all)