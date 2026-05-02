# app/managers.py

from app.db import supabase


def get_trades():
    response = supabase.table("trades").select("*").execute()
    return response.data


def create_trade(trade_data: dict):
    response = supabase.table("trades").insert(trade_data).execute()
    return response.data