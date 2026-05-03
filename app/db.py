from app.connection import supabase
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
from uuid import UUID

# Company DB Operations

async def get_companies_db():
    response = supabase.table("companies").select("*").execute()
    return response.data

async def get_company_db(company_id: UUID):
    response = supabase.table("companies").select("*").eq("id", company_id).execute()
    return response.data

async def add_company_db(company: CompanyBase):
    company_data = company.model_dump()
    response = supabase.table("companies").insert(company_data).execute()
    return response.data

async def update_company_db(company: CompanyBase, company_id: UUID):
    company_data = company.model_dump(exclude_unset=True)
    response = supabase.table("companies").update(company_data).eq("id", company_id).execute()
    return response.data

async def delete_company_db(company_id: UUID):
    response = supabase.table("companies").delete().eq("id", company_id).execute()
    return response.data

async def delete_companies_db():
    response = supabase.table("companies").delete().neq("id", "00000000-0000-0000-0000-000000000000").execute()
    return response.data   

# Shareholder DB Operations

async def get_shareholders_db():
    response = supabase.table("shareholders").select("*").execute()
    return response.data

async def get_shareholder_db(shareholder_id: UUID):
    response = supabase.table("shareholders").select("*").eq("id", shareholder_id).execute()
    return response.data

async def add_shareholder_db(shareholder: ShareholderBase):
    shareholder_data = shareholder.model_dump(mode="json")
    response = supabase.table("shareholders").insert(shareholder_data).execute()
    return response.data

async def update_shareholder_db(shareholder: ShareholderBase, shareholder_id: UUID):
    shareholder_data = shareholder.model_dump(mode="json", exclude_unset=True)
    response = supabase.table("shareholders").update(shareholder_data).eq("id", shareholder_id).execute()
    return response.data

async def delete_shareholder_db(shareholder_id: UUID):
    response = supabase.table("shareholders").delete().eq("id", shareholder_id).execute()
    return response.data

async def delete_shareholders_db():
    response = supabase.table("shareholders").delete().neq("id", "00000000-0000-0000-0000-000000000000").execute()
    return response.data   