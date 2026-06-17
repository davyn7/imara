# app/auth/db.py

from app.connection import supabase
from app.auth.schemas import UserBase

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
