# app/counterparties/db.py

from app.connection import supabase
from app.counterparties.schemas import CounterpartyBase, SPABase

# Counterparty DB Operations

async def get_counterparties_db():
    response = supabase.table("counterparties").select("*").execute()
    return response.data

async def get_counterparty_db(counterparty_id: int):
    response = supabase.table("counterparties").select("*").eq("id", counterparty_id).execute()
    return response.data

async def add_counterparty_db(counterparty: CounterpartyBase):
    counterparty_data = counterparty.model_dump(mode="json")
    response = supabase.table("counterparties").insert(counterparty_data).execute()
    return response.data

async def update_counterparty_db(counterparty: CounterpartyBase, counterparty_id: int):
    counterparty_data = counterparty.model_dump(mode="json", exclude_unset=True)
    response = supabase.table("counterparties").update(counterparty_data).eq("id", counterparty_id).execute()
    return response.data

async def delete_counterparty_db(counterparty_id: int):
    response = supabase.table("counterparties").delete().eq("id", counterparty_id).execute()
    return response.data

async def delete_counterparties_db():
    response = supabase.table("counterparties").delete().neq("id", 0).execute()
    return response.data

# SPA DB Operations

async def get_spas_db():
    response = supabase.table("spas").select("*").execute()
    return response.data

async def get_spa_db(spa_id: int):
    response = supabase.table("spas").select("*").eq("id", spa_id).execute()
    return response.data

async def add_spa_db(spa: SPABase):
    spa_data = spa.model_dump(mode="json")
    response = supabase.table("spas").insert(spa_data).execute()
    return response.data

async def update_spa_db(spa: SPABase, spa_id: int):
    spa_data = spa.model_dump(mode="json", exclude_unset=True)
    response = supabase.table("spas").update(spa_data).eq("id", spa_id).execute()
    return response.data

async def delete_spa_db(spa_id: int):
    response = supabase.table("spas").delete().eq("id", spa_id).execute()
    return response.data

async def delete_spas_db():
    response = supabase.table("spas").delete().neq("id", 0).execute()
    return response.data
