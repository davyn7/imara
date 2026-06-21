# app/trades/router.py

from fastapi import APIRouter
from app.trades.managers import TradeManager, TradeLegManager, TradeItemManager, TradeCostManager
from app.trades.schemas import (
    TradeCreate,
    TradeUpdate,
    TradeLegCreate,
    TradeLegUpdate,
    TradeItemCreate,
    TradeItemUpdate,
    TradeBase,
    TradeCostBase,
)


router = APIRouter(prefix="/trades", tags=["Trades"])


# ============================================================
# Trades
# ============================================================

@router.post("")
async def create_trade(trade: TradeCreate):
    try:
        manager = TradeManager(trade)
        return await manager.create_trade()
    except Exception as e:
        raise e


@router.get("")
async def get_trades():
    try:
        manager = TradeManager()
        return await manager.get_trades()
    except Exception as e:
        raise e


@router.get("/{trade_id}")
async def get_trade(trade_id: int):
    try:
        manager = TradeManager()
        return await manager.get_trade(trade_id)
    except Exception as e:
        raise e


@router.patch("/{trade_id}")
async def update_trade(trade_id: int, trade: TradeUpdate):
    try:
        manager = TradeManager(trade)
        return await manager.update_trade(trade_id)
    except Exception as e:
        raise e


@router.delete("/{trade_id}")
async def delete_trade(trade_id: int):
    try:
        manager = TradeManager()
        return await manager.delete_trade(trade_id)
    except Exception as e:
        raise e


@router.post("/{trade_id}/close")
async def close_trade(trade_id: int):
    try:
        manager = TradeManager()
        return await manager.close_trade(trade_id)
    except Exception as e:
        raise e


@router.post("/{trade_id}/cancel")
async def cancel_trade(trade_id: int):
    try:
        manager = TradeManager()
        return await manager.cancel_trade(trade_id)
    except Exception as e:
        raise e


@router.post("/{trade_id}/dispute")
async def dispute_trade(trade_id: int):
    try:
        manager = TradeManager()
        return await manager.dispute_trade(trade_id)
    except Exception as e:
        raise e


# ============================================================
# Trade Legs
# ============================================================

@router.post("/legs/{trade_leg_id}/fulfill")
async def fulfill_trade_leg(trade_leg_id: int):
    try:
        manager = TradeLegManager()
        return await manager.fulfill_trade_leg(trade_leg_id)
    except Exception as e:
        raise e


@router.post("/legs/{trade_leg_id}/cancel")
async def cancel_trade_leg(trade_leg_id: int):
    try:
        manager = TradeLegManager()
        return await manager.cancel_trade_leg(trade_leg_id)
    except Exception as e:
        raise e


@router.get("/legs/{trade_leg_id}")
async def get_trade_leg(trade_leg_id: int):
    try:
        manager = TradeLegManager()
        return await manager.get_trade_leg(trade_leg_id)
    except Exception as e:
        raise e


@router.patch("/legs/{trade_leg_id}")
async def update_trade_leg(trade_leg_id: int, trade_leg: TradeLegUpdate):
    try:
        manager = TradeLegManager(trade_leg)
        return await manager.update_trade_leg(trade_leg_id)
    except Exception as e:
        raise e


@router.delete("/legs/{trade_leg_id}")
async def delete_trade_leg(trade_leg_id: int):
    try:
        manager = TradeLegManager()
        return await manager.delete_trade_leg(trade_leg_id)
    except Exception as e:
        raise e


@router.post("/{trade_id}/legs")
async def create_trade_leg(trade_id: int, trade_leg: TradeLegCreate):
    try:
        manager = TradeLegManager(trade_leg)
        return await manager.create_trade_leg(trade_id)
    except Exception as e:
        raise e


@router.get("/{trade_id}/legs")
async def get_trade_legs(trade_id: int):
    try:
        manager = TradeLegManager()
        return await manager.get_trade_legs(trade_id)
    except Exception as e:
        raise e


# ============================================================
# Trade Items
# ============================================================

@router.get("/items/{trade_item_id}")
async def get_trade_item(trade_item_id: int):
    try:
        manager = TradeItemManager()
        return await manager.get_trade_item(trade_item_id)
    except Exception as e:
        raise e


@router.patch("/items/{trade_item_id}")
async def update_trade_item(trade_item_id: int, trade_item: TradeItemUpdate):
    try:
        manager = TradeItemManager(trade_item)
        return await manager.update_trade_item(trade_item_id)
    except Exception as e:
        raise e


@router.delete("/items/{trade_item_id}")
async def delete_trade_item(trade_item_id: int):
    try:
        manager = TradeItemManager()
        return await manager.delete_trade_item(trade_item_id)
    except Exception as e:
        raise e


@router.post("/{trade_id}/items")
async def create_trade_item(trade_id: int, trade_item: TradeItemCreate):
    try:
        manager = TradeItemManager(trade_item)
        return await manager.create_trade_item(trade_id)
    except Exception as e:
        raise e


@router.get("/{trade_id}/items")
async def get_trade_items(trade_id: int):
    try:
        manager = TradeItemManager()
        return await manager.get_trade_items(trade_id)
    except Exception as e:
        raise e


# ============================================================
# Trade Costs
# ============================================================

@router.post("/{trade_id}/costs")
async def create_trade_cost(trade_id: int):
    pass


@router.get("/{trade_id}/costs")
async def get_trade_costs(trade_id: int):
    pass


@router.get("/costs/{trade_cost_id}")
async def get_trade_cost(trade_cost_id: int):
    pass


@router.patch("/costs/{trade_cost_id}")
async def update_trade_cost(trade_cost_id: int):
    pass


@router.delete("/costs/{trade_cost_id}")
async def delete_trade_cost(trade_cost_id: int):
    pass


@router.post("/costs/{trade_cost_id}/mark-actual")
async def mark_trade_cost_as_actual(trade_cost_id: int):
    pass


@router.post("/costs/{trade_cost_id}/mark-paid")
async def mark_trade_cost_as_paid(trade_cost_id: int):
    pass


# ============================================================
# Trade Revenues
# ============================================================

@router.post("/{trade_id}/revenues")
async def create_trade_revenue(trade_id: int):
    pass


@router.get("/{trade_id}/revenues")
async def get_trade_revenues(trade_id: int):
    pass


@router.get("/revenues/{trade_revenue_id}")
async def get_trade_revenue(trade_revenue_id: int):
    pass


@router.patch("/revenues/{trade_revenue_id}")
async def update_trade_revenue(trade_revenue_id: int):
    pass


@router.delete("/revenues/{trade_revenue_id}")
async def delete_trade_revenue(trade_revenue_id: int):
    pass


@router.post("/revenues/{trade_revenue_id}/mark-actual")
async def mark_trade_revenue_as_actual(trade_revenue_id: int):
    pass


# ============================================================
# Trade Status Events
# ============================================================

@router.post("/{trade_id}/status-events")
async def create_trade_status_event(trade_id: int):
    pass


@router.get("/{trade_id}/status-events")
async def get_trade_status_events(trade_id: int):
    pass


@router.get("/status-events/{status_event_id}")
async def get_trade_status_event(status_event_id: int):
    pass


@router.patch("/status-events/{status_event_id}")
async def update_trade_status_event(status_event_id: int):
    pass


@router.delete("/status-events/{status_event_id}")
async def delete_trade_status_event(status_event_id: int):
    pass


# ============================================================
# Trade Notes
# ============================================================

@router.post("/{trade_id}/notes")
async def create_trade_note(trade_id: int):
    pass


@router.get("/{trade_id}/notes")
async def get_trade_notes(trade_id: int):
    pass


@router.get("/notes/{note_id}")
async def get_trade_note(note_id: int):
    pass


@router.patch("/notes/{note_id}")
async def update_trade_note(note_id: int):
    pass


@router.delete("/notes/{note_id}")
async def delete_trade_note(note_id: int):
    pass


# ============================================================
# Trade Summaries
# ============================================================

@router.get("/{trade_id}/margin")
async def get_trade_margin_summary(trade_id: int):
    pass


@router.get("/{trade_id}/cashflow")
async def get_trade_cashflow_summary(trade_id: int):
    pass


@router.get("/{trade_id}/overview")
async def get_trade_overview(trade_id: int):
    pass

# Trade Routers

@router.get("/trades")
async def get_trades():
    try:
        manager = TradeManager(None)
        return await manager.get_trades()
    except Exception as e:
        raise e

@router.get("/trades/{trade_id}")
async def get_trade(trade_id: int):
    try:
        manager = TradeManager(None)
        return await manager.get_trade(trade_id)
    except Exception as e:
        raise e

@router.post("/add_trade")
async def add_trade(trade: TradeBase):
    try:
        manager = TradeManager(trade)
        return await manager.add_trade()
    except Exception as e:
        raise e

@router.put("/update_trade/{trade_id}")
async def update_trade(trade_id: int, trade: TradeBase):
    try:
        manager = TradeManager(trade)
        return await manager.update_trade(trade_id)
    except Exception as e:
        raise e

@router.delete("/delete_trade/{trade_id}")
async def delete_trade(trade_id: int):
    try:
        manager = TradeManager(None)
        return await manager.delete_trade(trade_id)
    except Exception as e:
        raise e

@router.delete("/delete_trades")
async def delete_trades():
    try:
        manager = TradeManager(None)
        return await manager.delete_trades()
    except Exception as e:
        raise e

# Trade Cost Routers

@router.get("/trade_costs")
async def get_trade_costs():
    try:
        manager = TradeCostManager(None)
        return await manager.get_trade_costs()
    except Exception as e:
        raise e

@router.get("/trade_costs/{trade_cost_id}")
async def get_trade_cost(trade_cost_id: int):
    try:
        manager = TradeCostManager(None)
        return await manager.get_trade_cost(trade_cost_id)
    except Exception as e:
        raise e

@router.post("/add_trade_cost")
async def add_trade_cost(trade_cost: TradeCostBase):
    try:
        manager = TradeCostManager(trade_cost)
        return await manager.add_trade_cost()
    except Exception as e:
        raise e

@router.put("/update_trade_cost/{trade_cost_id}")
async def update_trade_cost(trade_cost_id: int, trade_cost: TradeCostBase):
    try:
        manager = TradeCostManager(trade_cost)
        return await manager.update_trade_cost(trade_cost_id)
    except Exception as e:
        raise e

@router.delete("/delete_trade_cost/{trade_cost_id}")
async def delete_trade_cost(trade_cost_id: int):
    try:
        manager = TradeCostManager(None)
        return await manager.delete_trade_cost(trade_cost_id)
    except Exception as e:
        raise e

@router.delete("/delete_trade_costs")
async def delete_trade_costs():
    try:
        manager = TradeCostManager(None)
        return await manager.delete_trade_costs()
    except Exception as e:
        raise e
