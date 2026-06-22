import asyncio
import random
import time
from datetime import datetime, timedelta, timezone

from faker import Faker
from passlib.context import CryptContext
from sqlalchemy import select, delete

from database import new_session
from models.auth import UserOrm
from models.music import (
    GenreOrm,
    TrackOrm,
    PlaylistOrm,
    playlist_tracks,
    FavoriteTrackOrm,
    DislikedTrackOrm,
    SavedPlaylistOrm
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
fake = Faker()

NUM_USERS = 800
NUM_TRACKS = 2000
NUM_PLAYLISTS = 300
NUM_FAVORITES = 40000
NUM_DISLIKED = 5000
NUM_SAVED_PLAYLISTS = 1500

ADJECTIVES = [
    "Neon", "Electric", "Golden", "Midnight", "Crimson", "Blue", "Dark", "Silent",
    "Broken", "Fading", "Lonely", "Endless", "Frozen", "Crystal", "Burning", "Lost",
    "Dancing", "Whispering", "Falling", "Eternal"
]
NOUNS = [
    "Dreams", "Shadows", "Lights", "Fire", "Rain", "Ocean", "Thunder", "Echoes",
    "Memories", "Hearts", "Waves", "Stars", "Secrets", "Voices", "Flames", "Horizons",
    "Rhythm", "Symphony", "Melody", "Silence"
]
ARTIST_NAMES = [
    "The Wandering Souls", "Echo Bloom", "Neon Mirage", "Crimson Tide", "Frostbite",
    "Silver Horizon", "Aurora Falls", "Ghost Choir", "Amber Waves", "Lunar Drift",
    "Crystal Visions", "Shadow Puppets", "Rusty Gears", "Velvet Thunder", "Iron Bloom",
    "Paper Kites", "Magnetic North", "Lost Satellites", "Ember Glow", "Static Pulse"
]

GENRE_CONFIG = {
    "pop": (1980, 2024),
    "rock": (1980, 2024),
    "hip-hop": (1990, 2024),
    "electronic": (1990, 2024),
    "jazz": (1950, 2020),
    "classical": (1950, 2000)
}


def generate_track_title():
    """Генерирует уникальное название трека с добавлением случайного числового суффикса"""
    a = random.choice(ADJECTIVES)
    b = random.choice(NOUNS)
    base = f"{a} {b}"
    if random.random() < 0.3:
        c = random.choice(NOUNS)
        base = f"{a} {b} {c}"
    suffix = random.randint(1, 9999)
    return f"{base} #{suffix}"


def generate_artist_name():
    """Возвращает имя исполнителя из заготовленного списка или сгенерированное Faker"""
    if random.random() < 0.5:
        return random.choice(ARTIST_NAMES)
    return fake.name()


def random_date(start_year=2020, end_year=2024):
    """Создаёт случайную дату в указанном диапазоне лет с учётом UTC"""
    start = datetime(start_year, 1, 1, tzinfo=timezone.utc)
    end = datetime(end_year, 12, 31, 23, 59, 59, tzinfo=timezone.utc)
    delta = end - start
    random_seconds = random.randint(0, int(delta.total_seconds()))
    return start + timedelta(seconds=random_seconds)


async def clear_tables():
    """Удаляет все записи из таблиц проекта перед новой генерацией"""
    print("Очистка таблиц...")
    async with new_session() as session:
        await session.execute(delete(SavedPlaylistOrm))
        await session.execute(delete(DislikedTrackOrm))
        await session.execute(delete(FavoriteTrackOrm))
        await session.execute(delete(playlist_tracks))
        await session.execute(delete(PlaylistOrm))
        await session.execute(delete(TrackOrm))
        await session.execute(delete(GenreOrm))
        await session.execute(delete(UserOrm))
        await session.commit()
    print("Таблицы очищены")


async def generate_all():
    """Основная функция генерации и записи тестовых данных в БД"""
    start_time = time.time()
    await clear_tables()

    async with new_session() as session:
        # Жанры
        print("Генерация жанров...")
        genres = []
        for name, (year_min, year_max) in GENRE_CONFIG.items():
            g = GenreOrm(name=name)
            session.add(g)
            genres.append(g)
        await session.commit()
        genre_dict = {g.name: g.id for g in genres}
        print(f"Жанров создано: {len(genres)}")

        # Пользователи
        print(f"Генерация {NUM_USERS} пользователей...")
        users = []
        for i in range(NUM_USERS):
            username = fake.user_name()
            email = fake.unique.email()
            hashed_password = pwd_context.hash("password")
            is_admin = (i == 0)
            created_at = random_date(2021, 2024)
            user = UserOrm(
                username=username,
                email=email,
                hashed_password=hashed_password,
                is_confirmed=True,
                is_admin=is_admin,
                created_at=created_at
            )
            session.add(user)
            users.append(user)
            if (i + 1) % 200 == 0:
                await session.flush()
        await session.commit()
        user_ids = [u.id for u in users]
        print(f"Пользователей создано: {len(users)}")

        # Треки
        print(f"Генерация {NUM_TRACKS} треков...")
        genre_track_counts = {
            "pop": 400,
            "rock": 400,
            "hip-hop": 350,
            "electronic": 350,
            "jazz": 250,
            "classical": 250
        }
        tracks = []
        track_count = 0
        for genre_name, count in genre_track_counts.items():
            genre_id = genre_dict[genre_name]
            year_min, year_max = GENRE_CONFIG[genre_name]
            for _ in range(count):
                title = generate_track_title()
                artist = generate_artist_name()
                year = random.randint(year_min, year_max)
                uploaded_by = random.choice(user_ids)
                uploaded_at = random_date(2020, 2024)
                track = TrackOrm(
                    title=title,
                    artist=artist,
                    genre_id=genre_id,
                    year=year,
                    uploaded_by=uploaded_by,
                    uploaded_at=uploaded_at
                )
                session.add(track)
                tracks.append(track)
                track_count += 1
                if track_count % 500 == 0:
                    await session.flush()
                    print(f"  Треков создано: {track_count}/{NUM_TRACKS}")
        await session.commit()
        track_ids = [t.id for t in tracks]
        print(f"Треков создано: {len(tracks)}")

        # Плейлисты
        print(f"Генерация плейлистов (цель ~{NUM_PLAYLISTS})...")
        playlists = []
        for user_id in user_ids:
            if random.random() < 0.4:
                num_user_playlists = random.randint(1, 3)
                for _ in range(num_user_playlists):
                    name = " ".join(fake.words(nb=random.randint(2, 4))).title()
                    is_public = random.choice([True, False])
                    created_at = random_date(2021, 2024)
                    playlist = PlaylistOrm(
                        user_id=user_id,
                        name=name,
                        is_public=is_public,
                        created_at=created_at
                    )
                    session.add(playlist)
                    playlists.append(playlist)
        await session.commit()
        playlist_ids = [p.id for p in playlists]
        print(f"Плейлистов создано: {len(playlists)}")

        # Наполнение плейлистов треками
        print("Наполнение плейлистов треками...")
        playlist_track_entries = []
        for idx, playlist in enumerate(playlists):
            num_tracks = random.randint(5, 30)
            chosen = random.sample(track_ids, min(num_tracks, len(track_ids)))
            for track_id in chosen:
                playlist_track_entries.append({
                    "playlist_id": playlist.id,
                    "track_id": track_id
                })
            if (idx + 1) % 100 == 0:
                print(f"  Обработано плейлистов: {idx+1}/{len(playlists)}")

        chunk_size = 1000
        for i in range(0, len(playlist_track_entries), chunk_size):
            chunk = playlist_track_entries[i:i + chunk_size]
            stmt = playlist_tracks.insert().values(chunk)
            await session.execute(stmt)
        await session.commit()
        print(f"Связей плейлист-трек создано: {len(playlist_track_entries)}")

        # Лайки
        print(f"Генерация лайков (цель {NUM_FAVORITES})...")
        young_genres = {"hip-hop", "electronic", "pop"}
        adult_genres = {"rock", "jazz", "classical", "pop"}

        user_age_group = {}
        for user_id in user_ids:
            user_age_group[user_id] = 0 if random.random() < 0.4 else 1

        genre_tracks = {g_id: [] for g_id in genre_dict.values()}
        for t in tracks:
            genre_tracks[t.genre_id].append(t.id)

        def get_preferred_genres(group):
            if group == 0:
                return [genre_dict[name] for name in young_genres]
            else:
                return [genre_dict[name] for name in adult_genres]

        like_set = set()
        likes_batch = []
        while len(like_set) < NUM_FAVORITES:
            user_id = random.choice(user_ids)
            group = user_age_group[user_id]
            preferred = get_preferred_genres(group)
            if random.random() < 0.7 and preferred:
                genre_id = random.choice(preferred)
            else:
                genre_id = random.choice(list(genre_dict.values()))
            possible_tracks = genre_tracks[genre_id]
            if not possible_tracks:
                continue
            track_id = random.choice(possible_tracks)
            pair = (user_id, track_id)
            if pair not in like_set:
                like_set.add(pair)
                created_at = random_date(2022, 2024)
                likes_batch.append(FavoriteTrackOrm(
                    user_id=user_id,
                    track_id=track_id,
                    created_at=created_at
                ))
                if len(likes_batch) >= 2000:
                    session.add_all(likes_batch)
                    await session.commit()
                    print(f"  Лайков создано: {len(like_set)}/{NUM_FAVORITES}")
                    likes_batch = []
        if likes_batch:
            session.add_all(likes_batch)
            await session.commit()
        print(f"Лайков создано: {len(like_set)}")

        # Дизлайки (исправленная версия с проверкой на пересечение)
        print(f"Генерация дизлайков (цель {NUM_DISLIKED})...")
        dislikes_set = set()
        dislikes_batch = []
        while len(dislikes_set) < NUM_DISLIKED:
            user_id = random.choice(user_ids)
            group = user_age_group[user_id]
            preferred = get_preferred_genres(group)
            if random.random() < 0.6 and preferred:
                non_preferred = [g for g in genre_dict.values() if g not in preferred]
                if non_preferred:
                    genre_id = random.choice(non_preferred)
                else:
                    genre_id = random.choice(list(genre_dict.values()))
            else:
                genre_id = random.choice(list(genre_dict.values()))
            possible_tracks = genre_tracks[genre_id]
            if not possible_tracks:
                continue
            track_id = random.choice(possible_tracks)
            pair = (user_id, track_id)
            # Исключаем треки, уже лайкнутые этим пользователем
            if pair in like_set or pair in dislikes_set:
                continue
            dislikes_set.add(pair)
            created_at = random_date(2022, 2024)
            dislikes_batch.append(DislikedTrackOrm(
                user_id=user_id,
                track_id=track_id,
                created_at=created_at
            ))
            if len(dislikes_batch) >= 1000:
                session.add_all(dislikes_batch)
                await session.commit()
                print(f"  Дизлайков создано: {len(dislikes_set)}/{NUM_DISLIKED}")
                dislikes_batch = []
        if dislikes_batch:
            session.add_all(dislikes_batch)
            await session.commit()
        print(f"Дизлайков создано: {len(dislikes_set)}")

        # Сохранённые плейлисты
        print(f"Генерация сохранённых плейлистов (цель {NUM_SAVED_PLAYLISTS})...")
        saved_set = set()
        saved_batch = []
        while len(saved_set) < NUM_SAVED_PLAYLISTS:
            user_id = random.choice(user_ids)
            playlist_id = random.choice(playlist_ids)
            playlist_owner = None
            for p in playlists:
                if p.id == playlist_id:
                    playlist_owner = p.user_id
                    break
            if playlist_owner == user_id:
                continue
            pair = (user_id, playlist_id)
            if pair not in saved_set:
                saved_set.add(pair)
                created_at = random_date(2022, 2024)
                saved_batch.append(SavedPlaylistOrm(
                    user_id=user_id,
                    playlist_id=playlist_id,
                    created_at=created_at
                ))
                if len(saved_batch) >= 1000:
                    session.add_all(saved_batch)
                    await session.commit()
                    print(f"  Сохранённых плейлистов: {len(saved_set)}/{NUM_SAVED_PLAYLISTS}")
                    saved_batch = []
        if saved_batch:
            session.add_all(saved_batch)
            await session.commit()
        print(f"Сохранённых плейлистов создано: {len(saved_set)}")

    elapsed = time.time() - start_time
    print(f"\nГенерация завершена за {elapsed:.1f} сек.")


if __name__ == "__main__":
    asyncio.run(generate_all())