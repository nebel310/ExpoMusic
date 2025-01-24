from pydantic import BaseModel, ConfigDict, EmailStr
from datetime import datetime




class SUserRegister(BaseModel):
    username: str
    email: EmailStr
    password: str
    password_confirm: str

class SUserLogin(BaseModel):
    email: EmailStr
    password: str

class SUser(BaseModel):
    id: int
    username: str
    email: EmailStr
    created_at: str  # Ожидаем строку
    is_active: bool

    model_config = ConfigDict(from_attributes=True)

    @classmethod
    def from_orm(cls, obj):
        # Преобразуем created_at в строку
        obj.created_at = str(obj.created_at)
        return super().from_orm(obj)