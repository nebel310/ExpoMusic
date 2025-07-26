import uvicorn
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from database import create_tables, delete_tables, new_session
from models.auth import create_initial_user
from models.music import create_initial_music_data
from router.auth import router as auth_router
from router.music import track_router, genre_router, playlist_router, library_router
from router.search import search_router




async def init_db():
    await create_tables()
    async with new_session() as session:
        await create_initial_user(session)
        await create_initial_music_data(session)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await delete_tables()
    print('База очищена')
    await create_tables()
    print('База готова к работе')
    
    async with new_session() as session:
        await create_initial_user(session)
        await create_initial_music_data(session)
    
    print('Занесены тестовые данные в базу данных')
    yield
    print('Выключение')


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Your App",
        version="1.0.0",
        description="API for users",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "Bearer": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
    }
    
    secured_paths = {
        #Авторизация
        "/auth/me": {"method": "get", "security": [{"Bearer": []}]},
        "/auth/logout": {"method": "post", "security": [{"Bearer": []}]},
        #Треки
        "/tracks": {"method": "post", "security": [{"Bearer": []}]},
        #Плейлисты
        "/playlists": {"method": "post", "security": [{"Bearer": []}]},
        "/playlists/update/{playlist_id}": {"method": "put", "security": [{"Bearer": []}]},
        "/playlists/remove/{playlist_id}": {"method": "delete", "security": [{"Bearer": []}]},
        "/playlists/add-track": {"method": "post", "security": [{"Bearer": []}]},
        "/playlists/remove-track": {"method": "post", "security": [{"Bearer": []}]},
        #"Моя медиатека"
        "/library/favorites/add/{track_id}": {"method": "post", "security": [{"Bearer": []}]},
        "/library/favorites/remove/{track_id}": {"method": "post", "security": [{"Bearer": []}]},
        "/library/favorites": {"method": "get", "security": [{"Bearer": []}]},
        "/library/disliked/add/{track_id}": {"method": "post", "security": [{"Bearer": []}]},
        "/library/disliked/remove/{track_id}": {"method": "post", "security": [{"Bearer": []}]},
        "/library/disliked": {"method": "get", "security": [{"Bearer": []}]},
        "/library/save/{playlist_id}": {"method": "post", "security": [{"Bearer": []}]},
        "/library/unsave/{playlist_id}": {"method": "post", "security": [{"Bearer": []}]},
        "/library/saved": {"method": "get", "security": [{"Bearer": []}]},
        #Поиск
        "/search": {"method": "get", "security": [{"Bearer": []}]},
    }
    
    for path, config in secured_paths.items():
        if path in openapi_schema["paths"]:
            openapi_schema["paths"][path][config["method"]]["security"] = config["security"]
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app = FastAPI(lifespan=lifespan)
app.openapi = custom_openapi
app.include_router(auth_router)
app.include_router(track_router)
app.include_router(genre_router)
app.include_router(playlist_router)
app.include_router(library_router)
app.include_router(search_router)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500"],  # Тут адрес фронтенда
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        reload=True,
        port=3001,
        #host="0.0.0.0"
    )