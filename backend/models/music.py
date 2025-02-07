from datetime import datetime, timezone
from sqlalchemy import ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from database import Model




class TrackOrm(Model):
    __tablename__ = 'tracks'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    uploaded_by: Mapped[int] = mapped_column(ForeignKey('users.id'))
    title: Mapped[str] = mapped_column(nullable=False, unique=True)
    artist: Mapped[str] = mapped_column(nullable=False)
    genre_id: Mapped[int] = mapped_column(ForeignKey('genres.id'), nullable=False, default=1)
    uploaded_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


class GenreOrm(Model):
    __tablename__ = 'genres'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True, nullable=False)