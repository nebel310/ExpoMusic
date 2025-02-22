from datetime import datetime, timezone
from sqlalchemy import ForeignKey, DateTime, Table, Column, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Model




class PlaylistOrm(Model):
    __tablename__ = 'playlists'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    name: Mapped[str] = mapped_column(nullable=False)
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
    title: Mapped[str] = mapped_column(nullable=False, unique=True)
    artist: Mapped[str] = mapped_column(nullable=False)
    genre_id: Mapped[int] = mapped_column(ForeignKey('genres.id'), nullable=False, default=1)
    uploaded_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    
    playlists = relationship("PlaylistOrm", secondary="playlist_tracks", back_populates="tracks")


class GenreOrm(Model):
    __tablename__ = 'genres'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True, nullable=False)