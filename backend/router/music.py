from fastapi import APIRouter, Depends, HTTPException
from schemas import STrack, STrackUpload, SGenre, SAddGenre, SPlaylist, SPlaylistCreate, SPlaylistUpdate, SPlaylistTrack, SSuccessResponse
from repositories.music import TrackRepository, GenreRepository, PlaylistRepository
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

playlist_router = APIRouter(
    prefix="/playlists",
    tags=['Плейлисты']
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

'''
----------------------------------------------
'''



'''
----------------------------------------------
Маршруты плейлистов
'''

@playlist_router.post("", response_model=SPlaylist)
async def create_playlist(playlist_data: SPlaylistCreate, current_user: UserOrm = Depends(get_current_user)):
    playlist = await PlaylistRepository.create_playlist(playlist_data, current_user.id)
    return SPlaylist.model_validate(playlist)


@playlist_router.get("/{playlist_id}", response_model=SPlaylist)
async def get_playlist(playlist_id: int):
    playlist = await PlaylistRepository.get_playlist_by_id(playlist_id)
    if not playlist:
        raise HTTPException(status_code=404, detail="Плейлист не найден")
    return SPlaylist.model_validate(playlist)


@playlist_router.put("/{playlist_id}", response_model=SPlaylist)
async def update_playlist(playlist_id: int, playlist_data: SPlaylistUpdate, current_user: UserOrm = Depends(get_current_user)):
    playlist = await PlaylistRepository.update_playlist(playlist_id, playlist_data)
    if not playlist:
        raise HTTPException(status_code=404, detail="Плейлист не найден")
    return SPlaylist.model_validate(playlist)


@playlist_router.delete("/{playlist_id}")
async def delete_playlist(playlist_id: int, current_user: UserOrm = Depends(get_current_user)):
    await PlaylistRepository.delete_playlist(playlist_id)
    return {"success": True, "message": "Плейлист удалён"}


@playlist_router.post("/add-track")
async def add_track_to_playlist(playlist_track_data: SPlaylistTrack, current_user: UserOrm = Depends(get_current_user)):
    await PlaylistRepository.add_track_to_playlist(playlist_track_data)
    return {"success": True, "message": "Трек добавлен в плейлист"}


@playlist_router.post("/remove-track", response_model=SSuccessResponse)
async def remove_track_from_playlist(playlist_track_data: SPlaylistTrack, current_user: UserOrm = Depends(get_current_user)):
    await PlaylistRepository.remove_track_from_playlist(playlist_track_data)
    return {"success": True, "message": "Трек удалён из плейлиста"}