# app/internal/db.py

from app.connection import supabase
from app.internal.schemas import CompanyBase, UserBase

# Company DB Operations

async def get_companies_db():
    response = supabase.table("companies").select("*").execute()
    return response.data

async def get_company_db(company_id: int):
    response = supabase.table("companies").select("*").eq("id", company_id).execute()
    return response.data

async def add_company_db(company: CompanyBase):
    company_data = company.model_dump()
    response = supabase.table("companies").insert(company_data).execute()
    return response.data

async def update_company_db(company: CompanyBase, company_id: int):
    company_data = company.model_dump(exclude_unset=True)
    response = supabase.table("companies").update(company_data).eq("id", company_id).execute()
    return response.data

async def delete_company_db(company_id: int):
    response = supabase.table("companies").delete().eq("id", company_id).execute()
    return response.data

async def delete_companies_db():
    response = supabase.table("companies").delete().neq("id", 0).execute()
    return response.data

# User DB Operations

async def get_users_db():
    response = supabase.table("users").select("*").execute()
    return response.data

async def get_user_db(user_id: int):
    response = supabase.table("users").select("*").eq("id", user_id).execute()
    return response.data

async def add_user_db(user: UserBase):
    user_data = user.model_dump(mode="json")
    response = supabase.table("users").insert(user_data).execute()
    return response.data

async def update_user_db(user: UserBase, user_id: int):
    user_data = user.model_dump(mode="json", exclude_unset=True)
    response = supabase.table("users").update(user_data).eq("id", user_id).execute()
    return response.data

async def delete_user_db(user_id: int):
    response = supabase.table("users").delete().eq("id", user_id).execute()
    return response.data

async def delete_users_db():
    response = supabase.table("users").delete().neq("id", 0).execute()
    return response.data
