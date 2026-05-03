# app/managers.py

from app.schemas import (
    ActivityLogBase,
    CompanyBase,
    CounterpartyBase,
    TradeBase,
    TradeCostBase,
    BrokerageDealBase,
    ShipmentBase,
    EquityRoundBase,
    ShareholderBase,
    ShareTransactionBase
)
from app.db import (
    get_companies_db,
    get_company_db,
    add_company_db,
    update_company_db,
    delete_company_db,
    delete_companies_db,
    get_shareholders_db,
    get_shareholder_db,
    add_shareholder_db,
    update_shareholder_db,
    delete_shareholder_db,
    delete_shareholders_db
)
from uuid import UUID

# Company Manager

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

    async def delete_companies(self):
        return await delete_companies_db()

# Shareholder Manager

class ShareholderManager:
    def __init__(self, shareholder: ShareholderBase):
        self.shareholder = shareholder
    
    async def get_shareholders(self):
        return await get_shareholders_db()

    async def get_shareholder(self, shareholder_id: UUID):
        return await get_shareholder_db(shareholder_id)

    async def add_shareholder(self):
        return await add_shareholder_db(self.shareholder)
    
    async def update_shareholder(self, shareholder_id: UUID):
        return await update_shareholder_db(self.shareholder, shareholder_id)
    
    async def delete_shareholder(self, shareholder_id: UUID):
        return await delete_shareholder_db(shareholder_id)

    async def delete_shareholders(self):
        return await delete_shareholders_db()

# def get_trades():
#     response = supabase.table("trades").select("*").execute()
#     return response.data


# def create_trade(trade_data: dict):
#     response = supabase.table("trades").insert(trade_data).execute()
#     return response.data