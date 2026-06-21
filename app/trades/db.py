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


def _active_legs(legs: list) -> list:
    return [
        leg
        for leg in legs
        if leg.get("status") != TradeLegStatus.CANCELLED.value
    ]


def _legs_summary_for_type(legs: list, leg_type: TradeLegType) -> dict:
    typed_legs = [
        leg for leg in _active_legs(legs) if leg.get("leg_type") == leg_type.value
    ]
    total_contract_value = sum(
        (_to_decimal(leg.get("total_price")) for leg in typed_legs),
        Decimal("0"),
    )
    fulfilled_legs = [
        leg for leg in typed_legs if leg.get("status") == TradeLegStatus.FULFILLED.value
    ]
    fulfilled_value = sum(
        (_to_decimal(leg.get("total_price")) for leg in fulfilled_legs),
        Decimal("0"),
    )
    outstanding_legs = [
        leg
        for leg in typed_legs
        if leg.get("status") != TradeLegStatus.FULFILLED.value
    ]
    outstanding_value = sum(
        (_to_decimal(leg.get("total_price")) for leg in outstanding_legs),
        Decimal("0"),
    )
    total_quantity = sum(
        (_to_decimal(leg.get("quantity")) for leg in typed_legs),
        Decimal("0"),
    )

    return {
        "leg_count": len(typed_legs),
        "fulfilled_count": len(fulfilled_legs),
        "outstanding_count": len(outstanding_legs),
        "total_contract_value": float(total_contract_value),
        "fulfilled_value": float(fulfilled_value),
        "outstanding_contract_value": float(outstanding_value),
        "total_quantity": float(total_quantity),
    }


async def get_trade_costs_summary_db(trade_id: int):
    trade_data = await get_trade_db(trade_id)
    if not trade_data:
        return None

    costs = await get_trade_costs_by_trade_db(trade_id)
    by_category: dict[str, dict] = {}

    for cost in costs:
        category = cost.get("category") or "other"
        if category not in by_category:
            by_category[category] = {
                "category": category,
                "count": 0,
                "estimated_total": Decimal("0"),
                "actual_total": Decimal("0"),
                "paid_total": Decimal("0"),
                "unpaid_count": 0,
            }

        amount = _amount_in_base(cost)
        by_category[category]["count"] += 1
        if cost.get("is_estimated"):
            by_category[category]["estimated_total"] += amount
        else:
            by_category[category]["actual_total"] += amount
        if cost.get("paid_date"):
            by_category[category]["paid_total"] += amount
        else:
            by_category[category]["unpaid_count"] += 1

    categories = []
    for category in sorted(by_category):
        entry = by_category[category]
        categories.append(
            {
                "category": entry["category"],
                "count": entry["count"],
                "estimated_total": float(entry["estimated_total"]),
                "actual_total": float(entry["actual_total"]),
                "paid_total": float(entry["paid_total"]),
                "unpaid_count": entry["unpaid_count"],
            }
        )

    return {
        "trade_id": trade_id,
        "base_currency": trade_data[0].get("base_currency") or "",
        "total_estimated_costs": float(
            sum((entry["estimated_total"] for entry in categories), 0.0)
        ),
        "total_actual_costs": float(
            sum((entry["actual_total"] for entry in categories), 0.0)
        ),
        "categories": categories,
    }


async def get_trade_legs_summary_db(trade_id: int):
    trade_data = await get_trade_db(trade_id)
    if not trade_data:
        return None

    legs = await get_trade_legs_db(trade_id)
    active = _active_legs(legs)
    purchase = _legs_summary_for_type(legs, TradeLegType.PURCHASE)
    sale = _legs_summary_for_type(legs, TradeLegType.SALE)

    fulfilled_count = purchase["fulfilled_count"] + sale["fulfilled_count"]
    active_count = purchase["leg_count"] + sale["leg_count"]
    fulfillment_progress = (
        float(fulfilled_count / active_count) if active_count else None
    )

    return {
        "trade_id": trade_id,
        "base_currency": trade_data[0].get("base_currency") or "",
        "purchase": purchase,
        "sale": sale,
        "fulfillment_progress": fulfillment_progress,
        "outstanding_contract_value": purchase["outstanding_contract_value"]
        + sale["outstanding_contract_value"],
        "legs_by_status": dict(Counter(leg.get("status") for leg in legs)),
    }


async def get_trade_treasury_cashflow_summary_db(trade_id: int):
    from app.treasury.db import get_trade_cashflow_summary_db as get_treasury_trade_cashflow_db

    trade_data = await get_trade_db(trade_id)
    if not trade_data:
        return None

    treasury = await get_treasury_trade_cashflow_db(trade_id)
    trade_cashflow = await get_trade_cashflow_summary_db(trade_id)

    treasury_inflows = treasury.get("total_receivables", 0) + treasury.get(
        "total_inflows", 0
    )
    treasury_outflows = treasury.get("total_payables", 0) + treasury.get(
        "total_outflows", 0
    )

    return {
        "trade_id": trade_id,
        "base_currency": trade_data[0].get("base_currency") or "",
        "treasury": treasury,
        "trade_cashflow": trade_cashflow,
        "treasury_net_position": treasury_inflows - treasury_outflows,
        "trade_net_position": trade_cashflow.get("net_actual_cashflow", 0)
        if trade_cashflow
        else 0,
        "combined_net_position": (treasury_inflows - treasury_outflows)
        + (trade_cashflow.get("net_actual_cashflow", 0) if trade_cashflow else 0),
    }


async def get_trades_portfolio_summary_db(
    company_id: int | None = None,
    status: str | None = None,
):
    query = supabase.table("trades").select("*")
    if company_id is not None:
        query = query.eq("imara_entity_id", company_id)
    if status is not None:
        query = query.eq("status", status)
    trades = query.execute().data

    total_estimated_gross_profit = Decimal("0")
    total_actual_gross_profit = Decimal("0")
    total_estimated_revenue = Decimal("0")
    total_open_cashflow_exposure = Decimal("0")
    trades_by_status: Counter = Counter()
    trade_rows = []

    for trade in trades:
        trade_id = trade["id"]
        margin = await get_trade_margin_summary_db(trade_id)
        cashflow = await get_trade_cashflow_summary_db(trade_id)
        trades_by_status[trade.get("status")] += 1

        if margin:
            total_estimated_gross_profit += Decimal(
                str(margin["estimated_gross_profit"])
            )
            total_actual_gross_profit += Decimal(str(margin["actual_gross_profit"]))
            total_estimated_revenue += Decimal(str(margin["estimated_revenue"]))

        if cashflow:
            total_open_cashflow_exposure += Decimal(
                str(cashflow["net_estimated_cashflow"])
            )

        trade_rows.append(
            {
                "trade_id": trade_id,
                "trade_code": trade.get("trade_code"),
                "status": trade.get("status"),
                "commodity": trade.get("commodity"),
                "margin_summary": margin,
                "cashflow_summary": cashflow,
            }
        )

    weighted_margin = _margin_percentage(
        total_estimated_gross_profit, total_estimated_revenue
    )

    return {
        "filters": {
            "company_id": company_id,
            "status": status,
        },
        "trade_count": len(trades),
        "trades_by_status": dict(trades_by_status),
        "total_estimated_gross_profit": float(total_estimated_gross_profit),
        "total_actual_gross_profit": float(total_actual_gross_profit),
        "weighted_estimated_margin_percentage": weighted_margin,
        "total_open_cashflow_exposure": float(total_open_cashflow_exposure),
        "trades": trade_rows,
    }


async def get_trade_settlement_status_db(trade_id: int):
    trade_data = await get_trade_db(trade_id)
    if not trade_data:
        return None

    trade = trade_data[0]
    margin = await get_trade_margin_summary_db(trade_id)
    cashflow = await get_trade_cashflow_summary_db(trade_id)
    legs = await get_trade_legs_db(trade_id)
    costs = await get_trade_costs_by_trade_db(trade_id)
    revenues = await get_trade_revenues_by_trade_db(trade_id)

    unpaid_costs = [cost for cost in costs if not cost.get("paid_date")]
    estimated_costs = [cost for cost in costs if cost.get("is_estimated")]
    estimated_revenues = [revenue for revenue in revenues if revenue.get("is_estimated")]
    unfulfilled_legs = [
        leg
        for leg in _active_legs(legs)
        if leg.get("status") != TradeLegStatus.FULFILLED.value
    ]

    terminal_statuses = {
        TradeStatus.CLOSED.value,
        TradeStatus.CANCELLED.value,
    }
    blockers = []
    if trade.get("status") in terminal_statuses:
        blockers.append("trade_already_terminal")
    if estimated_revenues:
        blockers.append("estimated_revenues_remaining")
    if estimated_costs:
        blockers.append("estimated_costs_remaining")
    if unpaid_costs:
        blockers.append("unpaid_costs_remaining")
    if unfulfilled_legs:
        blockers.append("unfulfilled_legs_remaining")

    ready_to_close = len(blockers) == 0

    return {
        "trade_id": trade_id,
        "trade_status": trade.get("status"),
        "ready_to_close": ready_to_close,
        "blockers": blockers,
        "margin_summary": margin,
        "cashflow_summary": cashflow,
        "estimated_vs_actual_variance": {
            "revenue": float(
                Decimal(str(margin["actual_revenue"]))
                - Decimal(str(margin["estimated_revenue"]))
            )
            if margin
            else 0.0,
            "gross_profit": float(
                Decimal(str(margin["actual_gross_profit"]))
                - Decimal(str(margin["estimated_gross_profit"]))
            )
            if margin
            else 0.0,
        },
        "unpaid_cost_count": len(unpaid_costs),
        "unfulfilled_leg_count": len(unfulfilled_legs),
        "estimated_revenue_count": len(estimated_revenues),
        "estimated_cost_count": len(estimated_costs),
    }


async def get_trade_items_summary_db(trade_id: int):
    trade_data = await get_trade_db(trade_id)
    if not trade_data:
        return None

    items = await get_trade_items_db(trade_id)
    legs = await get_trade_legs_db(trade_id)

    item_qty_by_unit: Counter = Counter()
    leg_qty_by_unit: Counter = Counter()
    by_commodity: dict[str, dict] = {}

    for item in items:
        unit = item.get("quantity_unit") or "unknown"
        quantity = _to_decimal(item.get("quantity"))
        item_qty_by_unit[unit] += quantity

        commodity = item.get("commodity") or "unknown"
        if commodity not in by_commodity:
            by_commodity[commodity] = {
                "commodity": commodity,
                "item_count": 0,
                "total_quantity": Decimal("0"),
                "quantity_units": set(),
            }
        by_commodity[commodity]["item_count"] += 1
        by_commodity[commodity]["total_quantity"] += quantity
        by_commodity[commodity]["quantity_units"].add(unit)

    for leg in _active_legs(legs):
        unit = leg.get("quantity_unit") or "unknown"
        leg_qty_by_unit[unit] += _to_decimal(leg.get("quantity"))

    quantity_mismatches = []
    for unit in sorted(set(item_qty_by_unit) | set(leg_qty_by_unit)):
        item_qty = item_qty_by_unit.get(unit, Decimal("0"))
        leg_qty = leg_qty_by_unit.get(unit, Decimal("0"))
        if item_qty != leg_qty:
            quantity_mismatches.append(
                {
                    "quantity_unit": unit,
                    "item_quantity": float(item_qty),
                    "leg_quantity": float(leg_qty),
                    "difference": float(item_qty - leg_qty),
                }
            )

    commodities = []
    for commodity in sorted(by_commodity):
        entry = by_commodity[commodity]
        commodities.append(
            {
                "commodity": entry["commodity"],
                "item_count": entry["item_count"],
                "total_quantity": float(entry["total_quantity"]),
                "quantity_units": sorted(entry["quantity_units"]),
            }
        )

    return {
        "trade_id": trade_id,
        "item_count": len(items),
        "leg_count": len(_active_legs(legs)),
        "commodities": commodities,
        "quantity_by_unit": {
            unit: float(item_qty_by_unit[unit]) for unit in sorted(item_qty_by_unit)
        },
        "leg_quantity_by_unit": {
            unit: float(leg_qty_by_unit[unit]) for unit in sorted(leg_qty_by_unit)
        },
        "quantity_mismatches": quantity_mismatches,
        "has_quantity_mismatch": len(quantity_mismatches) > 0,
    }
