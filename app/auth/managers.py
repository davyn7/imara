# app/auth/managers.py

from app.auth.schemas import UserBase
from app.auth.db import (
    get_users_db,
    get_user_db,
    add_user_db,
    update_user_db,
    delete_user_db,
    delete_users_db,
)

# User Manager

class UserManager:
    def __init__(self, user: UserBase):
        self.user = user

    async def get_users(self):
        return await get_users_db()

    async def get_user(self, user_id: int):
        return await get_user_db(user_id)

    async def add_user(self):
        return await add_user_db(self.user)

    async def update_user(self, user_id: int):
        return await update_user_db(self.user, user_id)

    async def delete_user(self, user_id: int):
        return await delete_user_db(user_id)

    async def delete_users(self):
        return await delete_users_db()
