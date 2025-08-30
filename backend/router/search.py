from fastapi import APIRouter, Depends, HTTPException
from schemas import SSearchResult
from repositories.search import SearchRepository
from models.auth import UserOrm
from security import get_current_user




search_router = APIRouter(
    prefix="/search",
    tags=['Поиск']
)



@search_router.get("", response_model=SSearchResult)
async def search(
    q: str,
    tracks_limit: int = 5,
    playlists_limit: int = 3,
    genres_limit: int = 2,
    current_user: UserOrm = Depends(get_current_user)
):
    try:
        results = await SearchRepository.global_search(
            q, 
            tracks_limit, 
            playlists_limit, 
            genres_limit
        )
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))