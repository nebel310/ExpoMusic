from pydantic import BaseModel, ConfigDict, EmailStr
from datetime import datetime




class SUserRegister(BaseModel):
    username: str
    email: EmailStr
    password: str
    password_confirm: str
    is_confirmed: bool = False


class SUserConfirm(BaseModel):
    is_confirmed: bool= True


class SUserLogin(BaseModel):
    email: EmailStr
    password: str


class SUser(BaseModel):
    id: int
    username: str
    email: EmailStr
    is_confirmed: bool
    created_at: datetime
    is_active: bool

    model_config = ConfigDict(from_attributes=True)