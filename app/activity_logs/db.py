# app/activity_logs/db.py

from app.connection import supabase
from app.activity_logs.schemas import ActivityLogBase

async def get_activity_logs_db():
    response = supabase.table("activity_logs").select("*").execute()
    return response.data

async def get_activity_log_db(activity_log_id: int):
    response = supabase.table("activity_logs").select("*").eq("id", activity_log_id).execute()
    return response.data

async def add_activity_log_db(activity_log: ActivityLogBase):
    activity_log_data = activity_log.model_dump(mode="json", exclude_none=True)
    response = supabase.table("activity_logs").insert(activity_log_data).execute()
    return response.data
