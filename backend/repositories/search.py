from database import new_session
from models.music import TrackOrm, GenreOrm, PlaylistOrm
from sqlalchemy import select




class SearchRepository:
    @classmethod
    async def search_tracks(cls, query: str, limit: int = 10) -> list[TrackOrm]:
        async with new_session() as session:
            query_stmt = select(TrackOrm).where(
                (TrackOrm.title.ilike(f"%{query}%")) | 
                (TrackOrm.artist.ilike(f"%{query}%"))
            ).limit(limit)
            result = await session.execute(query_stmt)
            return result.scalars().all()


    @classmethod
    async def search_playlists(cls, query: str, limit: int = 5) -> list[PlaylistOrm]:
        async with new_session() as session:
            query_stmt = select(PlaylistOrm).where(
                PlaylistOrm.name.ilike(f"%{query}%")
            ).limit(limit)
            result = await session.execute(query_stmt)
            return result.scalars().all()


    @classmethod
    async def search_genres(cls, query: str, limit: int = 5) -> list[GenreOrm]:
        async with new_session() as session:
            query_stmt = select(GenreOrm).where(
                GenreOrm.name.ilike(f"%{query}%")
            ).limit(limit)
            result = await session.execute(query_stmt)
            return result.scalars().all()


    @classmethod
    async def global_search(cls, query: str, 
                          tracks_limit: int = 5, 
                          playlists_limit: int = 3,
                          genres_limit: int = 2) -> dict:
        tracks = await cls.search_tracks(query, tracks_limit)
        playlists = await cls.search_playlists(query, playlists_limit)
        genres = await cls.search_genres(query, genres_limit)
        
        return {
            "tracks": tracks,
            "playlists": playlists,
            "genres": genres
        }