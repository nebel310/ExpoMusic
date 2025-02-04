from datetime import datetime
from pydantic import BaseModel, ConfigDict, EmailStr
from fastapi import UploadFile




class SUser(BaseModel):
    id: int
    username: str
    email: EmailStr
    is_confirmed: bool
    is_admin: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
    

class SUserRegister(BaseModel):
    username: str
    email: EmailStr
    password: str
    password_confirm: str
    is_confirmed: bool = False
    is_admin: bool = False


class SUserLogin(BaseModel):
    email: EmailStr
    password: str




class STrack(BaseModel):
    id: int
    uploaded_by: int
    title: str
    artist: str
    file: UploadFile
    duration: int = 60 #секунды
    playlists: list | None = None


class STrackUpload(BaseModel):
    title: str
    artist: str
    file: UploadFile
    genre: str


class SPlaylist(BaseModel):
    id: int
    created_by: int
    title: str
    tracks: list | None = None