# app/logistics/managers.py

from app.logistics.schemas import ShipmentBase
from app.logistics.db import (
    get_shipments_db,
    get_shipment_db,
    add_shipment_db,
    update_shipment_db,
    delete_shipment_db,
    delete_shipments_db,
)

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
