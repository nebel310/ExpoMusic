from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from database import create_tables, delete_tables
from router.auth import router as auth_router
from router.music import track_router, genre_router, playlist_router





@asynccontextmanager
async def lifespan(app: FastAPI):
    await delete_tables()
    print('База очищена')
    await create_tables()
    print('База готова к работе')
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
    
    secured_paths = [
        "/auth/me",
        "/auth/logout",
        "/tracks",
        "/playlists",
        "/playlists/{playlist_id}",
        "/playlists/add-track",
        "/playlists/remove-track"
    ]

    for path in secured_paths:
        if path in openapi_schema["paths"]:
            if path == "/tracks":
                openapi_schema["paths"][path]["post"]["security"] = [{"Bearer": []}]
            elif path == "/playlists":
                openapi_schema["paths"][path]["post"]["security"] = [{"Bearer": []}]
            elif path == "/playlists/{playlist_id}":
                openapi_schema["paths"][path]["put"]["security"] = [{"Bearer": []}]
                openapi_schema["paths"][path]["delete"]["security"] = [{"Bearer": []}]
            elif path == "/playlists/add-track":
                openapi_schema["paths"][path]["post"]["security"] = [{"Bearer": []}]
            elif path == "/playlists/remove-track":
                openapi_schema["paths"][path]["post"]["security"] = [{"Bearer": []}]
            elif path == "/auth/me":
                openapi_schema["paths"][path]["get"]["security"] = [{"Bearer": []}]
            elif path == "/auth/logout":
                openapi_schema["paths"][path]["post"]["security"] = [{"Bearer": []}]
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app = FastAPI(lifespan=lifespan)
app.openapi = custom_openapi
app.include_router(auth_router)
app.include_router(track_router)
app.include_router(genre_router)
app.include_router(playlist_router)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500"],  # Тут адрес фронтенда
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)