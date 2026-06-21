# app/trades/db.py

from app.connection import supabase
from app.trades.schemas import (
    TradeCreate,
    TradeUpdate,
    TradeStatus,
    TradeCostBase,
)


def _serialize(model) -> dict:
    return model.model_dump(mode="json")


# Trade DB Operations

async def get_trades_db():
    response = supabase.table("trades").select("*").execute()
    return response.data

async def get_trade_db(trade_id: int):
    response = supabase.table("trades").select("*").eq("id", trade_id).execute()
    return response.data

async def add_trade_db(trade: TradeCreate):
    trade_data = _serialize(trade)
    response = supabase.table("trades").insert(trade_data).execute()
    return response.data

async def update_trade_db(trade: TradeUpdate, trade_id: int):
    trade_data = trade.model_dump(mode="json", exclude_unset=True)
    response = (
        supabase.table("trades")
        .update(trade_data)
        .eq("id", trade_id)
        .execute()
    )
    return response.data

async def delete_trade_db(trade_id: int):
    response = supabase.table("trades").delete().eq("id", trade_id).execute()
    return response.data

async def close_trade_db(trade_id: int):
    response = (
        supabase.table("trades")
        .update({"status": TradeStatus.CLOSED.value})
        .eq("id", trade_id)
        .execute()
    )
    return response.data

async def cancel_trade_db(trade_id: int):
    response = (
        supabase.table("trades")
        .update({"status": TradeStatus.CANCELLED.value})
        .eq("id", trade_id)
        .execute()
    )
    return response.data

async def dispute_trade_db(trade_id: int):
    response = (
        supabase.table("trades")
        .update({"status": TradeStatus.DISPUTED.value})
        .eq("id", trade_id)
        .execute()
    )
    return response.data

async def delete_trades_db():
    response = supabase.table("trades").delete().neq("id", 0).execute()
    return response.data

# Trade Cost DB Operations

async def get_trade_costs_db():
    response = supabase.table("trade_costs").select("*").execute()
    return response.data

async def get_trade_cost_db(trade_cost_id: int):
    response = supabase.table("trade_costs").select("*").eq("id", trade_cost_id).execute()
    return response.data

async def add_trade_cost_db(trade_cost: TradeCostBase):
    trade_cost_data = trade_cost.model_dump(mode="json")
    response = supabase.table("trade_costs").insert(trade_cost_data).execute()
    return response.data

async def update_trade_cost_db(trade_cost: TradeCostBase, trade_cost_id: int):
    trade_cost_data = trade_cost.model_dump(mode="json", exclude_unset=True)
    response = supabase.table("trade_costs").update(trade_cost_data).eq("id", trade_cost_id).execute()
    return response.data

async def delete_trade_cost_db(trade_cost_id: int):
    response = supabase.table("trade_costs").delete().eq("id", trade_cost_id).execute()
    return response.data

async def delete_trade_costs_db():
    response = supabase.table("trade_costs").delete().neq("id", 0).execute()
    return response.data
