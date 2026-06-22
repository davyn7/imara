# app/logistics/managers.py

from app.logistics.schemas import ShipmentCreate, ShipmentUpdate
from app.logistics.db import (
    get_shipments_db,
    get_shipment_db,
    get_shipments_by_trade_db,
    add_shipment_db,
    update_shipment_db,
    delete_shipment_db,
    book_shipment_db,
    mark_shipment_as_loading_db,
    mark_shipment_as_loaded_db,
    mark_shipment_as_in_transit_db,
    mark_shipment_as_arrived_db,
    mark_shipment_as_discharged_db,
    mark_shipment_as_delivered_db,
    close_shipment_db,
    cancel_shipment_db,
    delay_shipment_db,
    get_shipment_overview_db,
)


class ShipmentManager:
    def __init__(self, shipment: ShipmentCreate | ShipmentUpdate | None = None):
        self.shipment = shipment

    async def get_shipments(self):
        return await get_shipments_db()

    async def get_shipment(self, shipment_id: int):
        return await get_shipment_db(shipment_id)

    async def get_shipments_by_trade(self, trade_id: int):
        return await get_shipments_by_trade_db(trade_id)

    async def create_shipment(self):
        return await add_shipment_db(self.shipment)

    async def update_shipment(self, shipment_id: int):
        return await update_shipment_db(self.shipment, shipment_id)

    async def delete_shipment(self, shipment_id: int):
        return await delete_shipment_db(shipment_id)

    async def book_shipment(self, shipment_id: int):
        return await book_shipment_db(shipment_id)

    async def mark_shipment_as_loading(self, shipment_id: int):
        return await mark_shipment_as_loading_db(shipment_id)

    async def mark_shipment_as_loaded(self, shipment_id: int):
        return await mark_shipment_as_loaded_db(shipment_id)

    async def mark_shipment_as_in_transit(self, shipment_id: int):
        return await mark_shipment_as_in_transit_db(shipment_id)

    async def mark_shipment_as_arrived(self, shipment_id: int):
        return await mark_shipment_as_arrived_db(shipment_id)

    async def mark_shipment_as_discharged(self, shipment_id: int):
        return await mark_shipment_as_discharged_db(shipment_id)

    async def mark_shipment_as_delivered(self, shipment_id: int):
        return await mark_shipment_as_delivered_db(shipment_id)

    async def close_shipment(self, shipment_id: int):
        return await close_shipment_db(shipment_id)

    async def cancel_shipment(self, shipment_id: int):
        return await cancel_shipment_db(shipment_id)

    async def delay_shipment(self, shipment_id: int):
        return await delay_shipment_db(shipment_id)

    async def get_shipment_overview(self, shipment_id: int):
        return await get_shipment_overview_db(shipment_id)
