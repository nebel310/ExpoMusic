from fastapi import APIRouter, Depends, HTTPException
from schemas import STrack, STrackUpload, SGenre, SAddGenre
from repositories.music import TrackRepository, GenreRepository
from models.auth import UserOrm
from security import get_current_user




track_router = APIRouter(
    prefix="/tracks",
    tags=['Треки']
)

genre_router = APIRouter(
    prefix="/genres",
    tags=['Жанры']
)



'''
----------------------------------------------
Маршруты треков
'''

@track_router.get("", response_model=list[STrack])
async def get_all_tracks(limit: int=10, offset: int=0):
    try:
        tracks = await TrackRepository.get_all_tracks(limit, offset)
        return [STrack.model_validate(track) for track in tracks]
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@track_router.post("")
async def upload_new_track(track_data: STrackUpload, current_user: UserOrm = Depends(get_current_user)):
    try:
        await TrackRepository.upload_new_track(track_data, current_user.id)
        return {"success": True, "message": "Трек загружен"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@track_router.get("/{track_id}", response_model=STrack)
async def get_track_by_id(track_id: int):
    try:
        user = await TrackRepository.get_track_by_id(track_id)
        return STrack.model_validate(user)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@track_router.get("/genres/{genre_id}", response_model=list[STrack])
async def get_tracks_by_genre_id(genre_id: int, limit: int=10, offset: int=0):
    try:
        tracks = await TrackRepository.get_tracks_by_genre_id(genre_id, limit, offset)
        return [STrack.model_validate(track) for track in tracks]
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@track_router.delete("/{track_id}") #Маршрут будет доступен только администраторам
async def delete_track(track_id: int):
    try:
        await TrackRepository.delete_track(track_id)
        return {"success": True, "message": "Трек удалён"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

'''
----------------------------------------------
'''



'''
----------------------------------------------
Маршруты жанров
'''

@genre_router.get("", response_model=list[SGenre])
async def get_all_genres(limit: int=10, offset: int=0):
    try:
        genres = await GenreRepository.get_all_genres(limit, offset)
        return [SGenre.model_validate(genre) for genre in genres]
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@genre_router.post("")
async def add_genre(genre_data: SAddGenre):
    try:
        await GenreRepository.add_genre(genre_data)
        return {"success": True, "message": "Жанр создан"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))