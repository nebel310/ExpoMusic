from datetime import datetime, timezone
from sqlalchemy import ForeignKey, DateTime, Table, Column, select
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Model




class PlaylistOrm(Model):
    __tablename__ = 'playlists'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    name: Mapped[str] = mapped_column(nullable=False, index=True)
    is_public: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    
    tracks = relationship("TrackOrm", secondary="playlist_tracks", back_populates="playlists", cascade="all, delete")


playlist_tracks = Table(
    "playlist_tracks",
    Model.metadata,
    Column("playlist_id", ForeignKey("playlists.id"), primary_key=True),
    Column("track_id", ForeignKey("tracks.id"), primary_key=True),
)


class TrackOrm(Model):
    __tablename__ = 'tracks'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    uploaded_by: Mapped[int] = mapped_column(ForeignKey('users.id'))
    title: Mapped[str] = mapped_column(nullable=False, unique=True, index=True)
    artist: Mapped[str] = mapped_column(nullable=False, index=True)
    genre_id: Mapped[int] = mapped_column(ForeignKey('genres.id'), nullable=False, default=1)
    uploaded_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    
    playlists = relationship("PlaylistOrm", secondary="playlist_tracks", back_populates="tracks")


class GenreOrm(Model):
    __tablename__ = 'genres'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True, nullable=False, index=True)



class FavoriteTrackOrm(Model):
    __tablename__ = 'favorite_tracks'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    track_id: Mapped[int] = mapped_column(ForeignKey('tracks.id'))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


class DislikedTrackOrm(Model):
    __tablename__ = 'disliked_tracks'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    track_id: Mapped[int] = mapped_column(ForeignKey('tracks.id'))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


class SavedPlaylistOrm(Model):
    __tablename__ = 'saved_playlists'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    playlist_id: Mapped[int] = mapped_column(ForeignKey('playlists.id'))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    
    


async def create_initial_music_data(session):
    from .auth import UserOrm
    from .music import GenreOrm, TrackOrm, PlaylistOrm
    
    # Создаем жанры
    if not await session.scalar(select(GenreOrm)):
        genres = [
            GenreOrm(name="NoGenre"),
            GenreOrm(name="Rock"),
            GenreOrm(name="Pop"),
            GenreOrm(name="Hip-Hop")
        ]
        session.add_all(genres)
        await session.commit()
    
    # Получаем пользователя
    user = await session.scalar(select(UserOrm).where(UserOrm.email == "user@example.com"))
    if not user:
        return
    
    # Создаем треки
    if not await session.scalar(select(TrackOrm)):
        rock_genre = await session.scalar(select(GenreOrm).where(GenreOrm.name == "Rock"))
        pop_genre = await session.scalar(select(GenreOrm).where(GenreOrm.name == "Pop"))
        
        tracks = [
            TrackOrm(
                uploaded_by=user.id,
                title="Example Track 1",
                artist="Test Artist",
                genre_id=rock_genre.id
            ),
            TrackOrm(
                uploaded_by=user.id,
                title="Example Track 2",
                artist="Test Artist",
                genre_id=pop_genre.id
            )
        ]
        session.add_all(tracks)
        await session.commit()
    
    # Создаем плейлист
    if not await session.scalar(select(PlaylistOrm)):
        tracks = await session.scalars(select(TrackOrm))
        tracks_list = list(tracks.all())
        
        playlist = PlaylistOrm(
            user_id=user.id,
            name="Car Playlist",
            is_public=True
        )
        session.add(playlist)
        await session.commit()
        
        # Добавляем треки в плейлист через таблицу связи
        stmt = playlist_tracks.insert().values([
            {"playlist_id": playlist.id, "track_id": track.id}
            for track in tracks_list
        ])
        await session.execute(stmt)
        await session.commit()