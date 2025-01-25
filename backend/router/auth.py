from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from schemas import SUserRegister, SUserLogin, SUser
from repositories.auth import UserRepository
from database import UserOrm
from security import create_access_token, get_current_user

router = APIRouter(
    prefix="/auth",
    tags=['Пользователи']
)

@router.post("/register")
async def register_user(user_data: SUserRegister):
    try:
        user_id = await UserRepository.register_user(user_data)
        return {"success": True, "user_id": user_id}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login")
async def login_user(login_data: SUserLogin):
    user = await UserRepository.authenticate_user(login_data.email, login_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Неверный email или пароль")
    
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=SUser)
async def get_current_user_info(current_user: UserOrm = Depends(get_current_user)):
    return SUser.model_validate(current_user)