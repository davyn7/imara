# app/managers.py

from app.schemas import CompanyBase
from app.db import (
    get_companies_db,
    get_company_db,
    add_company_db,
    update_company_db,
    delete_company_db
)
from uuid import UUID

# Company Managers

class CompanyManager:
    def __init__(self, company: CompanyBase):
        self.company = company

    async def get_companies(self):
        return await get_companies_db()

    async def get_company(self, company_id: UUID):
        return await get_company_db(company_id)

    async def add_company(self):
        return await add_company_db(self.company)
    
    async def update_company(self, company_id: UUID):
        return await update_company_db(self.company, company_id)
    
    async def delete_company(self, company_id: UUID):
        return await delete_company_db(company_id)
        
# async def create_company(company_data: dict):
#     response = supabase.table("companies").insert(company_data).execute()
#     return response.data

# def get_trades():
#     response = supabase.table("trades").select("*").execute()
#     return response.data


# def create_trade(trade_data: dict):
#     response = supabase.table("trades").insert(trade_data).execute()
#     return response.data