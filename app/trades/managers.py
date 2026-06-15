# app/trades/managers.py

from app.trades.schemas import TradeBase, TradeCostBase, ShipmentBase
from app.trades.db import (
    get_trades_db,
    get_trade_db,
    add_trade_db,
    update_trade_db,
    delete_trade_db,
    delete_trades_db,
    get_trade_costs_db,
    get_trade_cost_db,
    add_trade_cost_db,
    update_trade_cost_db,
    delete_trade_cost_db,
    delete_trade_costs_db,
    get_shipments_db,
    get_shipment_db,
    add_shipment_db,
    update_shipment_db,
    delete_shipment_db,
    delete_shipments_db,
)

# Trade Manager

class TradeManager:
    def __init__(self, trade: TradeBase):
        self.trade = trade

    async def get_trades(self):
        return await get_trades_db()

    async def get_trade(self, trade_id: int):
        return await get_trade_db(trade_id)

    async def add_trade(self):
        return await add_trade_db(self.trade)

    async def update_trade(self, trade_id: int):
        return await update_trade_db(self.trade, trade_id)

    async def delete_trade(self, trade_id: int):
        return await delete_trade_db(trade_id)

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

# Shipment Manager

class ShipmentManager:
    def __init__(self, shipment: ShipmentBase):
        self.shipment = shipment

    async def get_shipments(self):
        return await get_shipments_db()

    async def get_shipment(self, shipment_id: int):
        return await get_shipment_db(shipment_id)

    async def add_shipment(self):
        return await add_shipment_db(self.shipment)

    async def update_shipment(self, shipment_id: int):
        return await update_shipment_db(self.shipment, shipment_id)

    async def delete_shipment(self, shipment_id: int):
        return await delete_shipment_db(shipment_id)

    async def delete_shipments(self):
        return await delete_shipments_db()
