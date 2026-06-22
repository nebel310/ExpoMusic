from passlib.context import CryptContext
from sqlalchemy import select
from database import new_session
from models.auth import UserOrm
from models.music import GenreOrm, TrackOrm, PlaylistOrm, playlist_tracks




pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")



async def create_test_data():
    DOES_NEED_USER = True
    DOES_NEED_MUSIC = True

    async def create_initial_user():
        async with new_session() as session:
            if not await session.scalar(select(UserOrm)):
                admin_user = UserOrm(
                    username="string",
                    email="user@example.com",
                    hashed_password=pwd_context.hash("string"),
                    is_confirmed=True,
                    is_admin=True
                )
                session.add(admin_user)
                await session.commit()


    async def create_initial_music_data():
        async with new_session() as session:
            # Жанры
            if not await session.scalar(select(GenreOrm)):
                genres = [
                    GenreOrm(name="NoGenre"),
                    GenreOrm(name="Rock"),
                    GenreOrm(name="Pop"),
                    GenreOrm(name="Hip-Hop")
                ]
                session.add_all(genres)
                await session.commit()

            # Пользователь
            user = await session.scalar(select(UserOrm).where(UserOrm.email == "user@example.com"))
            if not user:
                return

            # Треки
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

            # Плейлист
            if not await session.scalar(select(PlaylistOrm)):
                tracks_result = await session.scalars(select(TrackOrm))
                tracks_list = list(tracks_result.all())

                playlist = PlaylistOrm(
                    user_id=user.id,
                    name="Car Playlist",
                    is_public=True
                )
                session.add(playlist)
                await session.commit()

                stmt = playlist_tracks.insert().values([
                    {"playlist_id": playlist.id, "track_id": track.id}
                    for track in tracks_list
                ])
                await session.execute(stmt)
                await session.commit()

    if DOES_NEED_USER:
        await create_initial_user()

    if DOES_NEED_MUSIC:
        await create_initial_music_data()