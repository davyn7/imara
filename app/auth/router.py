# app/auth/router.py

from fastapi import APIRouter
from app.auth.managers import UserManager
from app.auth.schemas import UserBase

router = APIRouter(prefix="/auth", tags=["Auth"])

# User Routers

@router.get("/users")
async def get_users():
    try:
        manager = UserManager(None)
        return await manager.get_users()
    except Exception as e:
        raise e

@router.get("/users/{user_id}")
async def get_user(user_id: int):
    try:
        manager = UserManager(None)
        return await manager.get_user(user_id)
    except Exception as e:
        raise e

@router.post("/add_user")
async def add_user(user: UserBase):
    try:
        manager = UserManager(user)
        return await manager.add_user()
    except Exception as e:
        raise e

@router.put("/update_user/{user_id}")
async def update_user(user_id: int, user: UserBase):
    try:
        manager = UserManager(user)
        return await manager.update_user(user_id)
    except Exception as e:
        raise e

@router.delete("/delete_user/{user_id}")
async def delete_user(user_id: int):
    try:
        manager = UserManager(None)
        return await manager.delete_user(user_id)
    except Exception as e:
        raise e

@router.delete("/delete_users")
async def delete_users():
    try:
        manager = UserManager(None)
        return await manager.delete_users()
    except Exception as e:
        raise e
