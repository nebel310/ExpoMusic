from datetime import datetime
from pydantic import BaseModel, ConfigDict, EmailStr




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


class SRefresh(BaseModel):
    token: str

    class Config:
        json_schema_extra = {
            "example": {
                "token": "my_refresh_token"
            }
        }




class STrack(BaseModel):
    id: int
    uploaded_by: int
    title: str
    artist: str
    genre_id: int
    
    model_config = ConfigDict(from_attributes=True)


class STrackUpload(BaseModel):
    title: str
    artist: str
    genre_id: int


class SGenre(BaseModel):
    id: int
    name: str
    
    model_config = ConfigDict(from_attributes=True)
    

class SAddGenre(BaseModel):
    name: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "NoGenre"
            }
        }



class SPlaylist(BaseModel):
    id: int
    user_id: int
    name: str
    is_public: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class SPlaylistCreate(BaseModel):
    name: str
    is_public: bool = False

class SPlaylistUpdate(BaseModel):
    name: str | None = None
    is_public: bool | None = None

class SPlaylistTrack(BaseModel):
    playlist_id: int
    track_id: int


class SSuccessResponse(BaseModel):
    success: bool
    message: str