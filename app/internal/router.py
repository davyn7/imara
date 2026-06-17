# app/internal/router.py

from fastapi import APIRouter
from app.internal.managers import CompanyManager, UserManager
from app.internal.schemas import CompanyBase, UserBase

router = APIRouter(prefix="/internal", tags=["Internal"])

# Company Routers

@router.get("/companies")
async def get_companies():
    try:
        manager = CompanyManager(None)
        return await manager.get_companies()
    except Exception as e:
        raise e

@router.get("/companies/{company_id}")
async def get_company(company_id: int):
    try:
        manager = CompanyManager(None)
        return await manager.get_company(company_id)
    except Exception as e:
        raise e

@router.post("/add_company")
async def add_company(company: CompanyBase):
    try:
        manager = CompanyManager(company)
        return await manager.add_company()
    except Exception as e:
        raise e

@router.put("/update_company/{company_id}")
async def update_company(company_id: int, company: CompanyBase):
    try:
        manager = CompanyManager(company)
        return await manager.update_company(company_id)
    except Exception as e:
        raise e

@router.delete("/delete_company/{company_id}")
async def delete_company(company_id: int):
    try:
        manager = CompanyManager(None)
        return await manager.delete_company(company_id)
    except Exception as e:
        raise e

@router.delete("/delete_companies")
async def delete_companies():
    try:
        manager = CompanyManager(None)
        return await manager.delete_companies()
    except Exception as e:
        raise e

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
