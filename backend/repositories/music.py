from database import new_session
from models.music import TrackOrm, GenreOrm, PlaylistOrm, playlist_tracks
from schemas import STrack, STrackUpload, SAddGenre, SPlaylist, SPlaylistCreate, SPlaylistUpdate, SPlaylistTrack
from sqlalchemy import select, delete




class TrackRepository:
    @classmethod
    async def get_all_tracks(cls, limit: int, offset: int) -> list:
        async with new_session() as session:
            query = select(TrackOrm).limit(limit).offset(offset)
            result = await session.execute(query)
            tracks = result.scalars().all()
            return tracks
    
    
    @classmethod
    async def get_tracks_by_genre_id(cls, genre_id: int, limit: int, offset: int):
        async with new_session() as session:
            query = select(TrackOrm).where(TrackOrm.genre_id == genre_id).limit(limit).offset(offset)
            result = await session.execute(query)
            tracks = result.scalars().all()
            return tracks
    
    
    @classmethod
    async def get_track_by_id(cls, track_id:int) -> STrack | None:
        async with new_session() as session:
            query = select(TrackOrm).where(TrackOrm.id == track_id)
            result = await session.execute(query)
            
            track = result.scalars().first()
            if not track:
                raise ValueError('Трек не найден')
            
            return track
    
    
    @classmethod
    async def upload_new_track(cls, track_data: STrackUpload, uploaded_by: int):
        async with new_session() as session:
            query1 = select(TrackOrm).where(TrackOrm.title == track_data.title)
            result1 = await session.execute(query1)
            
            if result1.scalars().first():
                raise ValueError('Трек с таким названием уже существует')
            
            query2 = select(GenreOrm).where(GenreOrm.id == track_data.genre_id)     
            result2 = await session.execute(query2)
            
            if not result2.scalars().first():
                raise ValueError('Такого жанра не существует')
            
            track = TrackOrm(
                uploaded_by = uploaded_by,
                title = track_data.title,
                artist = track_data.artist,
                genre_id = track_data.genre_id
            )
            
            session.add(track)
            await session.flush()
            await session.commit()


    @classmethod
    async def delete_track(cls, track_id: int):
        async with new_session() as session:
            delete_tracks_query = delete(playlist_tracks).where(playlist_tracks.c.track_id == track_id)
            await session.execute(delete_tracks_query)

            delete_track_query = delete(TrackOrm).where(TrackOrm.id == track_id)
            result = await session.execute(delete_track_query)

            if result.rowcount == 0:
                raise ValueError('Трек не найден')

            await session.commit()




class GenreRepository:
    @classmethod
    async def get_all_genres(cls, limit: int, offset: int) -> list:
        async with new_session() as session:
            query = select(GenreOrm).limit(limit).offset(offset)
            result = await session.execute(query)
            genres = result.scalars().all()
            return genres
    
    
    @classmethod
    async def add_genre(cls, genre_data: SAddGenre):
        async with new_session() as session:
            query = select(GenreOrm).where(GenreOrm.name == genre_data.name)
            result = await session.execute(query)
            if result.scalars().first():
                raise ValueError('Такой жанр уже существует')
            
            
            genre = GenreOrm(
                name = genre_data.name
            )
            
            session.add(genre)
            await session.flush()
            await session.commit()




class PlaylistRepository:
    @classmethod
    async def create_playlist(cls, playlist_data: SPlaylistCreate, user_id: int) -> PlaylistOrm:
        async with new_session() as session:
            playlist = PlaylistOrm(
                user_id=user_id,
                name=playlist_data.name,
                is_public=playlist_data.is_public
            )
            session.add(playlist)
            await session.flush()
            await session.commit()
            return playlist


    @classmethod
    async def get_playlist_by_id(cls, playlist_id: int) -> PlaylistOrm | None:
        async with new_session() as session:
            query = select(PlaylistOrm).where(PlaylistOrm.id == playlist_id)
            result = await session.execute(query)
            
            playlist = result.scalars().first()
            
            if not playlist:
                raise ValueError('Плейлист не найден')
            
            return playlist


    @classmethod
    async def update_playlist(cls, playlist_id: int, playlist_data: SPlaylistUpdate) -> PlaylistOrm | None:
        async with new_session() as session:
            query = select(PlaylistOrm).where(PlaylistOrm.id == playlist_id)
            result = await session.execute(query)
            playlist = result.scalars().first()
            
            if not playlist:
                raise ValueError("Плейлист не найден")
            
            if playlist_data.name is not None:
                playlist.name = playlist_data.name
            
            if playlist_data.is_public is not None:
                playlist.is_public = playlist_data.is_public
            
            await session.commit()
            return playlist


    @classmethod
    async def delete_playlist(cls, playlist_id: int):
        async with new_session() as session:
            delete_tracks_query = delete(playlist_tracks).where(playlist_tracks.c.playlist_id == playlist_id)
            await session.execute(delete_tracks_query)

            delete_playlist_query = delete(PlaylistOrm).where(PlaylistOrm.id == playlist_id)
            result = await session.execute(delete_playlist_query)

            if result.rowcount == 0:
                raise ValueError('Плейлист не найден')

            await session.commit()


    @classmethod
    async def add_track_to_playlist(cls, playlist_track_data: SPlaylistTrack):
        async with new_session() as session:
            try:
                stmt = playlist_tracks.insert().values(
                    playlist_id=playlist_track_data.playlist_id,
                    track_id=playlist_track_data.track_id
                )
                await session.execute(stmt)
                await session.commit()
            except:
                raise ValueError("Нельзя добавить в плейлисты одинаковые треки")


    @classmethod
    async def remove_track_from_playlist(cls, playlist_track_data: SPlaylistTrack):
        async with new_session() as session:
            stmt = playlist_tracks.delete().where(
                (playlist_tracks.c.playlist_id == playlist_track_data.playlist_id) &
                (playlist_tracks.c.track_id == playlist_track_data.track_id)
            )
            result = await session.execute(stmt)
            
            if result.rowcount == 0:
                raise ValueError('Трек в этом плейлисте не найден')
            
            await session.commit()