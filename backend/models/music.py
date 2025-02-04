from datetime import datetime, timezone
from sqlalchemy import ForeignKey, DateTime, Table, Column, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Model




playlist_tracks = Table(
    "playlist_tracks",
    Model.metadata,
    Column("playlist_id", Integer, ForeignKey("playlists.id"), primary_key=True),
    Column("track_id", Integer, ForeignKey("tracks.id"), primary_key=True),
)


class TrackOrm(Model):
    __tablename__ = 'tracks'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    uploaded_by: Mapped[int] = mapped_column(ForeignKey('users.id'))
    title: Mapped[str] = mapped_column(nullable=False, unique=True)
    artist: Mapped[str] = mapped_column(nullable=False)
    genre: Mapped[str] = mapped_column(ForeignKey('genres.name'), nullable=False)
    duration: Mapped[int] = mapped_column(nullable=False)
    file: Mapped[str] = mapped_column(nullable=False)
    playlists: Mapped[list["PlaylistOrm"]] = relationship(secondary=playlist_tracks, back_populates="tracks")
    uploaded_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


class PlaylistOrm(Model):
    __tablename__ = 'playlists'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(nullable=False)
    tracks: Mapped[list["TrackOrm"]] = relationship(secondary=playlist_tracks, back_populates="playlists")
    created_by: Mapped[int] = mapped_column(ForeignKey('users.id'))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


class GenreOrm(Model):
    __tablename__ = 'genres'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True, nullable=False)