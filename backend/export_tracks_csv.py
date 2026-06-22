"""
Скрипт экспорта треков в CSV.
Запускать локально при поднятой локальной PostgreSQL.
"""
import asyncio
import csv
import random
import os
from database import new_session
from models.music import TrackOrm, GenreOrm
from sqlalchemy import select


async def export_tracks_csv():
    """Выгружает треки из БД в data/tracks.csv с добавлением genre_name и duration"""
    os.makedirs("data", exist_ok=True)
    
    async with new_session() as session:
        stmt = (
            select(
                TrackOrm.id,
                TrackOrm.title,
                TrackOrm.artist,
                GenreOrm.name.label("genre_name"),
                TrackOrm.year,
                TrackOrm.uploaded_by,
                TrackOrm.uploaded_at
            )
            .join(GenreOrm, TrackOrm.genre_id == GenreOrm.id)
            .order_by(TrackOrm.id)
        )
        result = await session.execute(stmt)
        rows = result.all()
    
    with open("data/tracks.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["track_id", "title", "artist", "genre_name", "year", "duration", "uploaded_by", "uploaded_at"])
        for row in rows:
            track_id, title, artist, genre_name, year, uploaded_by, uploaded_at = row
            duration = random.randint(180, 300)  # заглушка
            writer.writerow([track_id, title, artist, genre_name, year, duration, uploaded_by, uploaded_at])
    
    print(f"Экспортировано треков: {len(rows)}")


if __name__ == "__main__":
    asyncio.run(export_tracks_csv())