# app/trades/router.py

from fastapi import APIRouter
from app.trades.managers import TradeManager, TradeCostManager
from app.trades.schemas import TradeBase, TradeCostBase

router = APIRouter(prefix="/trades", tags=["Trades"])

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
