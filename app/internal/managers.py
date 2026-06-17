# app/internal/managers.py

from app.internal.schemas import CompanyBase, UserBase
from app.internal.db import (
    get_companies_db,
    get_company_db,
    add_company_db,
    update_company_db,
    delete_company_db,
    delete_companies_db,
    get_users_db,
    get_user_db,
    add_user_db,
    update_user_db,
    delete_user_db,
    delete_users_db,
)

# Company Manager

class CompanyManager:
    def __init__(self, company: CompanyBase):
        self.company = company

    async def get_companies(self):
        return await get_companies_db()

    async def get_company(self, company_id: int):
        return await get_company_db(company_id)

    async def add_company(self):
        return await add_company_db(self.company)

    async def update_company(self, company_id: int):
        return await update_company_db(self.company, company_id)

    async def delete_company(self, company_id: int):
        return await delete_company_db(company_id)

    async def delete_companies(self):
        return await delete_companies_db()

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
