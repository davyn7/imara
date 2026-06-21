# app/trades/db.py

from collections import Counter
from datetime import date
from decimal import Decimal

from app.connection import supabase
from app.trades.schemas import (
    TradeCreate,
    TradeUpdate,
    TradeStatus,
    TradeLegCreate,
    TradeLegUpdate,
    TradeLegStatus,
    TradeLegType,
    TradeItemCreate,
    TradeItemUpdate,
    TradeCostCreate,
    TradeCostUpdate,
    TradeRevenueCreate,
    TradeRevenueUpdate,
    TradeStatusEventCreate,
    TradeStatusEventUpdate,
    TradeNoteCreate,
    TradeNoteUpdate,
)


def _serialize(model) -> dict:
    return model.model_dump(mode="json")


def _to_decimal(value) -> Decimal:
    if value is None:
        return Decimal("0")
    if isinstance(value, Decimal):
        return value
    return Decimal(str(value))


def _amount_in_base(record: dict) -> Decimal:
    base_amount = record.get("amount_base_currency")
    if base_amount is not None:
        return _to_decimal(base_amount)
    return _to_decimal(record.get("amount"))


def _margin_percentage(gross_profit: Decimal, revenue: Decimal):
    if revenue <= 0:
        return None
    return float((gross_profit / revenue) * 100)


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

# Trade Note DB Operations

async def get_trade_notes_db(trade_id: int):
    response = (
        supabase.table("trade_notes")
        .select("*")
        .eq("trade_id", trade_id)
        .execute()
    )
    return response.data

async def get_trade_note_db(note_id: int):
    response = (
        supabase.table("trade_notes")
        .select("*")
        .eq("id", note_id)
        .execute()
    )
    return response.data

async def add_trade_note_db(trade_id: int, trade_note: TradeNoteCreate):
    trade_note_data = _serialize(trade_note)
    trade_note_data["trade_id"] = trade_id
    response = supabase.table("trade_notes").insert(trade_note_data).execute()
    return response.data

async def update_trade_note_db(trade_note: TradeNoteUpdate, note_id: int):
    trade_note_data = trade_note.model_dump(mode="json", exclude_unset=True)
    response = (
        supabase.table("trade_notes")
        .update(trade_note_data)
        .eq("id", note_id)
        .execute()
    )
    return response.data

async def delete_trade_note_db(note_id: int):
    response = (
        supabase.table("trade_notes")
        .delete()
        .eq("id", note_id)
        .execute()
    )
    return response.data

# Trade Summary DB Operations

async def get_trade_margin_summary_db(trade_id: int):
    trade_data = await get_trade_db(trade_id)
    if not trade_data:
        return None

    trade = trade_data[0]
    base_currency = trade.get("base_currency") or ""

    revenues = await get_trade_revenues_by_trade_db(trade_id)
    costs = await get_trade_costs_by_trade_db(trade_id)
    legs = await get_trade_legs_db(trade_id)

    estimated_revenue = sum(
        (_amount_in_base(r) for r in revenues if r.get("is_estimated")),
        Decimal("0"),
    )
    actual_revenue = sum(
        (_amount_in_base(r) for r in revenues if not r.get("is_estimated")),
        Decimal("0"),
    )

    purchase_legs = [
        leg
        for leg in legs
        if leg.get("leg_type") == TradeLegType.PURCHASE.value
        and leg.get("status") != TradeLegStatus.CANCELLED.value
    ]
    estimated_purchase_cost = sum(
        (_to_decimal(leg.get("total_price")) for leg in purchase_legs),
        Decimal("0"),
    )
    actual_purchase_cost = sum(
        (
            _to_decimal(leg.get("total_price"))
            for leg in purchase_legs
            if leg.get("status") == TradeLegStatus.FULFILLED.value
        ),
        Decimal("0"),
    )

    estimated_trade_costs = sum(
        (_amount_in_base(c) for c in costs if c.get("is_estimated")),
        Decimal("0"),
    )
    actual_trade_costs = sum(
        (_amount_in_base(c) for c in costs if not c.get("is_estimated")),
        Decimal("0"),
    )

    estimated_gross_profit = (
        estimated_revenue - estimated_purchase_cost - estimated_trade_costs
    )
    actual_gross_profit = actual_revenue - actual_purchase_cost - actual_trade_costs

    return {
        "trade_id": trade_id,
        "base_currency": base_currency,
        "estimated_revenue": float(estimated_revenue),
        "estimated_purchase_cost": float(estimated_purchase_cost),
        "estimated_trade_costs": float(estimated_trade_costs),
        "estimated_gross_profit": float(estimated_gross_profit),
        "estimated_margin_percentage": _margin_percentage(
            estimated_gross_profit, estimated_revenue
        ),
        "actual_revenue": float(actual_revenue),
        "actual_purchase_cost": float(actual_purchase_cost),
        "actual_trade_costs": float(actual_trade_costs),
        "actual_gross_profit": float(actual_gross_profit),
        "actual_margin_percentage": _margin_percentage(
            actual_gross_profit, actual_revenue
        ),
    }


async def get_trade_cashflow_summary_db(trade_id: int):
    trade_data = await get_trade_db(trade_id)
    if not trade_data:
        return None

    trade = trade_data[0]
    base_currency = trade.get("base_currency") or ""

    revenues = await get_trade_revenues_by_trade_db(trade_id)
    costs = await get_trade_costs_by_trade_db(trade_id)

    total_estimated_inflows = sum(
        (_amount_in_base(r) for r in revenues if r.get("is_estimated")),
        Decimal("0"),
    )
    total_actual_inflows = sum(
        (_amount_in_base(r) for r in revenues if not r.get("is_estimated")),
        Decimal("0"),
    )
    total_estimated_outflows = sum(
        (_amount_in_base(c) for c in costs if c.get("is_estimated")),
        Decimal("0"),
    )
    total_actual_outflows = sum(
        (_amount_in_base(c) for c in costs if not c.get("is_estimated")),
        Decimal("0"),
    )
    total_paid_outflows = sum(
        (_amount_in_base(c) for c in costs if c.get("paid_date")),
        Decimal("0"),
    )

    unpaid_outflows = [cost for cost in costs if not cost.get("paid_date")]
    unpaid_outflows.sort(key=lambda cost: cost.get("due_date") or "")

    estimated_inflows = [
        revenue for revenue in revenues if revenue.get("is_estimated")
    ]
    estimated_inflows.sort(key=lambda revenue: revenue.get("revenue_date") or "")

    net_estimated_cashflow = total_estimated_inflows - total_estimated_outflows
    net_actual_cashflow = total_actual_inflows - total_actual_outflows

    return {
        "trade_id": trade_id,
        "base_currency": base_currency,
        "total_estimated_inflows": float(total_estimated_inflows),
        "total_actual_inflows": float(total_actual_inflows),
        "total_estimated_outflows": float(total_estimated_outflows),
        "total_actual_outflows": float(total_actual_outflows),
        "total_paid_outflows": float(total_paid_outflows),
        "net_estimated_cashflow": float(net_estimated_cashflow),
        "net_actual_cashflow": float(net_actual_cashflow),
        "unpaid_outflows": unpaid_outflows,
        "estimated_inflows": estimated_inflows,
    }


async def get_trade_overview_db(trade_id: int):
    trade_data = await get_trade_db(trade_id)
    if not trade_data:
        return None

    legs = await get_trade_legs_db(trade_id)
    items = await get_trade_items_db(trade_id)
    costs = await get_trade_costs_by_trade_db(trade_id)
    revenues = await get_trade_revenues_by_trade_db(trade_id)
    status_events = await get_trade_status_events_db(trade_id)
    notes = await get_trade_notes_db(trade_id)

    margin_summary = await get_trade_margin_summary_db(trade_id)
    cashflow_summary = await get_trade_cashflow_summary_db(trade_id)

    return {
        "trade": trade_data[0],
        "margin_summary": margin_summary,
        "cashflow_summary": cashflow_summary,
        "counts": {
            "legs": len(legs),
            "items": len(items),
            "costs": len(costs),
            "revenues": len(revenues),
            "status_events": len(status_events),
            "notes": len(notes),
        },
        "legs_by_status": dict(Counter(leg.get("status") for leg in legs)),
        "costs_by_category": dict(Counter(cost.get("category") for cost in costs)),
        "recent_status_events": status_events[-5:],
    }
