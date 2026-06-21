# app/trades/managers.py

from app.trades.schemas import TradeCreate, TradeUpdate, TradeCostBase
from app.trades.db import (
    get_trades_db,
    get_trade_db,
    add_trade_db,
    update_trade_db,
    delete_trade_db,
    close_trade_db,
    cancel_trade_db,
    dispute_trade_db,
    delete_trades_db,
    get_trade_costs_db,
    get_trade_cost_db,
    add_trade_cost_db,
    update_trade_cost_db,
    delete_trade_cost_db,
    delete_trade_costs_db,
)

# Trade Manager

class TradeManager:
    def __init__(self, trade: TradeCreate | TradeUpdate | None = None):
        self.trade = trade

    async def get_trades(self):
        return await get_trades_db()

    async def get_trade(self, trade_id: int):
        return await get_trade_db(trade_id)

    async def create_trade(self):
        return await add_trade_db(self.trade)

    async def add_trade(self):
        return await add_trade_db(self.trade)

    async def update_trade(self, trade_id: int):
        return await update_trade_db(self.trade, trade_id)

    async def delete_trade(self, trade_id: int):
        return await delete_trade_db(trade_id)

    async def close_trade(self, trade_id: int):
        return await close_trade_db(trade_id)

    async def cancel_trade(self, trade_id: int):
        return await cancel_trade_db(trade_id)

    async def dispute_trade(self, trade_id: int):
        return await dispute_trade_db(trade_id)

    async def delete_trades(self):
        return await delete_trades_db()

# Trade Cost Manager

class TradeCostManager:
    def __init__(self, trade_cost: TradeCostBase):
        self.trade_cost = trade_cost

    async def get_trade_costs(self):
        return await get_trade_costs_db()

    async def get_trade_cost(self, trade_cost_id: int):
        return await get_trade_cost_db(trade_cost_id)

    async def add_trade_cost(self):
        return await add_trade_cost_db(self.trade_cost)

    async def update_trade_cost(self, trade_cost_id: int):
        return await update_trade_cost_db(self.trade_cost, trade_cost_id)

    async def delete_trade_cost(self, trade_cost_id: int):
        return await delete_trade_cost_db(trade_cost_id)

    async def delete_trade_costs(self):
        return await delete_trade_costs_db()
