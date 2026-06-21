# app/trades/db.py

from datetime import date

from app.connection import supabase
from app.trades.schemas import (
    TradeCreate,
    TradeUpdate,
    TradeStatus,
    TradeLegCreate,
    TradeLegUpdate,
    TradeLegStatus,
    TradeItemCreate,
    TradeItemUpdate,
    TradeCostCreate,
    TradeCostUpdate,
    TradeRevenueCreate,
    TradeRevenueUpdate,
    TradeStatusEventCreate,
    TradeStatusEventUpdate,
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

# Trade Leg DB Operations

async def get_trade_legs_db(trade_id: int):
    response = (
        supabase.table("trade_legs")
        .select("*")
        .eq("trade_id", trade_id)
        .execute()
    )
    return response.data

async def get_trade_leg_db(trade_leg_id: int):
    response = (
        supabase.table("trade_legs")
        .select("*")
        .eq("id", trade_leg_id)
        .execute()
    )
    return response.data

async def add_trade_leg_db(trade_id: int, trade_leg: TradeLegCreate):
    trade_leg_data = _serialize(trade_leg)
    trade_leg_data["trade_id"] = trade_id
    response = supabase.table("trade_legs").insert(trade_leg_data).execute()
    return response.data

async def update_trade_leg_db(trade_leg: TradeLegUpdate, trade_leg_id: int):
    trade_leg_data = trade_leg.model_dump(mode="json", exclude_unset=True)
    response = (
        supabase.table("trade_legs")
        .update(trade_leg_data)
        .eq("id", trade_leg_id)
        .execute()
    )
    return response.data

async def delete_trade_leg_db(trade_leg_id: int):
    response = (
        supabase.table("trade_legs")
        .delete()
        .eq("id", trade_leg_id)
        .execute()
    )
    return response.data

async def fulfill_trade_leg_db(trade_leg_id: int):
    response = (
        supabase.table("trade_legs")
        .update({"status": TradeLegStatus.FULFILLED.value})
        .eq("id", trade_leg_id)
        .execute()
    )
    return response.data

async def cancel_trade_leg_db(trade_leg_id: int):
    response = (
        supabase.table("trade_legs")
        .update({"status": TradeLegStatus.CANCELLED.value})
        .eq("id", trade_leg_id)
        .execute()
    )
    return response.data

# Trade Item DB Operations

async def get_trade_items_db(trade_id: int):
    response = (
        supabase.table("trade_items")
        .select("*")
        .eq("trade_id", trade_id)
        .execute()
    )
    return response.data

async def get_trade_item_db(trade_item_id: int):
    response = (
        supabase.table("trade_items")
        .select("*")
        .eq("id", trade_item_id)
        .execute()
    )
    return response.data

async def add_trade_item_db(trade_id: int, trade_item: TradeItemCreate):
    trade_item_data = _serialize(trade_item)
    trade_item_data["trade_id"] = trade_id
    response = supabase.table("trade_items").insert(trade_item_data).execute()
    return response.data

async def update_trade_item_db(trade_item: TradeItemUpdate, trade_item_id: int):
    trade_item_data = trade_item.model_dump(mode="json", exclude_unset=True)
    response = (
        supabase.table("trade_items")
        .update(trade_item_data)
        .eq("id", trade_item_id)
        .execute()
    )
    return response.data

async def delete_trade_item_db(trade_item_id: int):
    response = (
        supabase.table("trade_items")
        .delete()
        .eq("id", trade_item_id)
        .execute()
    )
    return response.data

# Trade Cost DB Operations

async def get_trade_costs_db():
    response = supabase.table("trade_costs").select("*").execute()
    return response.data

async def get_trade_costs_by_trade_db(trade_id: int):
    response = (
        supabase.table("trade_costs")
        .select("*")
        .eq("trade_id", trade_id)
        .execute()
    )
    return response.data

async def get_trade_cost_db(trade_cost_id: int):
    response = supabase.table("trade_costs").select("*").eq("id", trade_cost_id).execute()
    return response.data

async def add_trade_cost_db(trade_cost: TradeCostCreate, trade_id: int | None = None):
    trade_cost_data = _serialize(trade_cost)
    if trade_id is not None:
        trade_cost_data["trade_id"] = trade_id
    response = supabase.table("trade_costs").insert(trade_cost_data).execute()
    return response.data

async def update_trade_cost_db(trade_cost: TradeCostUpdate, trade_cost_id: int):
    trade_cost_data = trade_cost.model_dump(mode="json", exclude_unset=True)
    response = (
        supabase.table("trade_costs")
        .update(trade_cost_data)
        .eq("id", trade_cost_id)
        .execute()
    )
    return response.data

async def delete_trade_cost_db(trade_cost_id: int):
    response = supabase.table("trade_costs").delete().eq("id", trade_cost_id).execute()
    return response.data

async def mark_trade_cost_as_actual_db(trade_cost_id: int):
    response = (
        supabase.table("trade_costs")
        .update({"is_estimated": False})
        .eq("id", trade_cost_id)
        .execute()
    )
    return response.data

async def mark_trade_cost_as_paid_db(trade_cost_id: int):
    response = (
        supabase.table("trade_costs")
        .update({"paid_date": date.today().isoformat()})
        .eq("id", trade_cost_id)
        .execute()
    )
    return response.data

async def delete_trade_costs_db():
    response = supabase.table("trade_costs").delete().neq("id", 0).execute()
    return response.data

# Trade Revenue DB Operations

async def get_trade_revenues_by_trade_db(trade_id: int):
    response = (
        supabase.table("trade_revenues")
        .select("*")
        .eq("trade_id", trade_id)
        .execute()
    )
    return response.data

async def get_trade_revenue_db(trade_revenue_id: int):
    response = (
        supabase.table("trade_revenues")
        .select("*")
        .eq("id", trade_revenue_id)
        .execute()
    )
    return response.data

async def add_trade_revenue_db(trade_revenue: TradeRevenueCreate, trade_id: int | None = None):
    trade_revenue_data = _serialize(trade_revenue)
    if trade_id is not None:
        trade_revenue_data["trade_id"] = trade_id
    response = supabase.table("trade_revenues").insert(trade_revenue_data).execute()
    return response.data

async def update_trade_revenue_db(trade_revenue: TradeRevenueUpdate, trade_revenue_id: int):
    trade_revenue_data = trade_revenue.model_dump(mode="json", exclude_unset=True)
    response = (
        supabase.table("trade_revenues")
        .update(trade_revenue_data)
        .eq("id", trade_revenue_id)
        .execute()
    )
    return response.data

async def delete_trade_revenue_db(trade_revenue_id: int):
    response = (
        supabase.table("trade_revenues")
        .delete()
        .eq("id", trade_revenue_id)
        .execute()
    )
    return response.data

async def mark_trade_revenue_as_actual_db(trade_revenue_id: int):
    response = (
        supabase.table("trade_revenues")
        .update({"is_estimated": False})
        .eq("id", trade_revenue_id)
        .execute()
    )
    return response.data

# Trade Status Event DB Operations

async def get_trade_status_events_db(trade_id: int):
    response = (
        supabase.table("trade_status_events")
        .select("*")
        .eq("trade_id", trade_id)
        .execute()
    )
    return response.data

async def get_trade_status_event_db(status_event_id: int):
    response = (
        supabase.table("trade_status_events")
        .select("*")
        .eq("id", status_event_id)
        .execute()
    )
    return response.data

async def add_trade_status_event_db(trade_id: int, status_event: TradeStatusEventCreate):
    status_event_data = _serialize(status_event)
    status_event_data["trade_id"] = trade_id
    response = supabase.table("trade_status_events").insert(status_event_data).execute()
    return response.data

async def update_trade_status_event_db(
    status_event: TradeStatusEventUpdate,
    status_event_id: int,
):
    status_event_data = status_event.model_dump(mode="json", exclude_unset=True)
    response = (
        supabase.table("trade_status_events")
        .update(status_event_data)
        .eq("id", status_event_id)
        .execute()
    )
    return response.data

async def delete_trade_status_event_db(status_event_id: int):
    response = (
        supabase.table("trade_status_events")
        .delete()
        .eq("id", status_event_id)
        .execute()
    )
    return response.data
