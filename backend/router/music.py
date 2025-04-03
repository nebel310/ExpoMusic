from fastapi import APIRouter, Depends, HTTPException
from schemas import STrack, STrackUpload, SGenre, SAddGenre, SPlaylist, SPlaylistCreate, SPlaylistUpdate, SPlaylistTrack, SSuccessResponse
from repositories.music import TrackRepository, GenreRepository, PlaylistRepository, FavoriteTrackRepository, DislikedTrackRepository, SavedPlaylistRepository
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

library_router = APIRouter(
    prefix="/library",
    tags=['Медиатека']
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
    try:
        playlist = await PlaylistRepository.create_playlist(playlist_data, current_user.id)
        return SPlaylist.model_validate(playlist)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@playlist_router.get("/{playlist_id}", response_model=SPlaylist)
async def get_playlist(playlist_id: int):
    try:
        playlist = await PlaylistRepository.get_playlist_with_tracks(playlist_id)
        return SPlaylist.model_validate(playlist)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@playlist_router.put("/update/{playlist_id}", response_model=SPlaylist)
async def update_playlist(playlist_id: int, playlist_data: SPlaylistUpdate, current_user: UserOrm = Depends(get_current_user)):
    try:
        playlist = await PlaylistRepository.update_playlist(playlist_id, playlist_data)
        return SPlaylist.model_validate(playlist)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@playlist_router.delete("/remove/{playlist_id}")
async def delete_playlist(playlist_id: int, current_user: UserOrm = Depends(get_current_user)):
    try:
        await PlaylistRepository.delete_playlist(playlist_id)
        return {"success": True, "message": "Плейлист удалён"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@playlist_router.post("/add-track")
async def add_track_to_playlist(playlist_track_data: SPlaylistTrack, current_user: UserOrm = Depends(get_current_user)):
    try:
        await PlaylistRepository.add_track_to_playlist(playlist_track_data)
        return {"success": True, "message": "Трек добавлен в плейлист"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@playlist_router.post("/remove-track", response_model=SSuccessResponse)
async def remove_track_from_playlist(playlist_track_data: SPlaylistTrack, current_user: UserOrm = Depends(get_current_user)):
    try:
        await PlaylistRepository.remove_track_from_playlist(playlist_track_data)
        return {"success": True, "message": "Трек удалён из плейлиста"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

'''
----------------------------------------------
'''



'''
----------------------------------------------
Маршруты для медиатеки
'''

@library_router.post("/favorites/add/{track_id}")
async def add_to_favorites(track_id: int, current_user: UserOrm = Depends(get_current_user)):
    try:
        await FavoriteTrackRepository.add_to_favorites(current_user.id, track_id)
        return {"success": True, "message": "Трек добавлен в избранное"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@library_router.post("/favorites/remove/{track_id}")
async def remove_from_favorites(track_id: int, current_user: UserOrm = Depends(get_current_user)):
    try:
        await FavoriteTrackRepository.remove_from_favorites(current_user.id, track_id)
        return {"success": True, "message": "Трек удален из избранного"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@library_router.get("/favorites", response_model=list[STrack])
async def get_favorite_tracks(limit: int = 10, offset: int = 0, current_user: UserOrm = Depends(get_current_user)):
    try:
        tracks = await FavoriteTrackRepository.get_favorite_tracks(current_user.id, limit, offset)
        return [STrack.model_validate(track) for track in tracks]
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@library_router.post("/disliked/add/{track_id}")
async def add_to_disliked(track_id: int, current_user: UserOrm = Depends(get_current_user)):
    try:
        await DislikedTrackRepository.add_to_disliked(current_user.id, track_id)
        return {"success": True, "message": "Трек добавлен в 'Не нравится'"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@library_router.post("/disliked/remove/{track_id}")
async def remove_from_disliked(track_id: int, current_user: UserOrm = Depends(get_current_user)):
    try:
        await DislikedTrackRepository.remove_from_disliked(current_user.id, track_id)
        return {"success": True, "message": "Трек удален из 'Не нравится'"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@library_router.get("/disliked", response_model=list[STrack])
async def get_disliked_tracks(limit: int = 10, offset: int = 0, current_user: UserOrm = Depends(get_current_user)):
    try:
        tracks = await DislikedTrackRepository.get_disliked_tracks(current_user.id, limit, offset)
        return [STrack.model_validate(track) for track in tracks]
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@library_router.post("/save/{playlist_id}")
async def save_playlist(playlist_id: int, current_user: UserOrm = Depends(get_current_user)):
    try:
        await SavedPlaylistRepository.save_playlist(current_user.id, playlist_id)
        return {"success": True, "message": "Плейлист сохранен"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@library_router.post("/unsave/{playlist_id}")
async def unsave_playlist(playlist_id: int, current_user: UserOrm = Depends(get_current_user)):
    try:
        await SavedPlaylistRepository.unsave_playlist(current_user.id, playlist_id)
        return {"success": True, "message": "Плейлист удален из сохраненных"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@library_router.get("/saved", response_model=list[SPlaylist])
async def get_saved_playlists(limit: int = 10, offset: int = 0, current_user: UserOrm = Depends(get_current_user)):
    try:
        playlists = await SavedPlaylistRepository.get_saved_playlists(current_user.id, limit, offset)
        return [SPlaylist.model_validate(playlist) for playlist in playlists]
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))