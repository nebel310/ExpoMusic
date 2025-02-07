from database import new_session
from models.music import TrackOrm, GenreOrm
from schemas import STrack, STrackUpload, SAddGenre
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
            query = select(TrackOrm).where(TrackOrm.title == track_data.title)
            result = await session.execute(query)
            
            if result.scalars().first():
                raise ValueError('Трек с таким названием уже существует')            
            
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
            query = delete(TrackOrm).where(TrackOrm.id == track_id)
            result = await session.execute(query)
            
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