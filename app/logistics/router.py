# app/logistics/router.py

from fastapi import APIRouter
from app.logistics.managers import ShipmentManager
from app.logistics.schemas import ShipmentBase

router = APIRouter(prefix="/logistics", tags=["Logistics"])

# Shipment Routers

@router.get("/shipments")
async def get_shipments():
    try:
        manager = ShipmentManager(None)
        return await manager.get_shipments()
    except Exception as e:
        raise e

@router.get("/shipments/{shipment_id}")
async def get_shipment(shipment_id: int):
    try:
        manager = ShipmentManager(None)
        return await manager.get_shipment(shipment_id)
    except Exception as e:
        raise e

@router.post("/add_shipment")
async def add_shipment(shipment: ShipmentBase):
    try:
        manager = ShipmentManager(shipment)
        return await manager.add_shipment()
    except Exception as e:
        raise e

@router.put("/update_shipment/{shipment_id}")
async def update_shipment(shipment_id: int, shipment: ShipmentBase):
    try:
        manager = ShipmentManager(shipment)
        return await manager.update_shipment(shipment_id)
    except Exception as e:
        raise e

@router.delete("/delete_shipment/{shipment_id}")
async def delete_shipment(shipment_id: int):
    try:
        manager = ShipmentManager(None)
        return await manager.delete_shipment(shipment_id)
    except Exception as e:
        raise e

@router.delete("/delete_shipments")
async def delete_shipments():
    try:
        manager = ShipmentManager(None)
        return await manager.delete_shipments()
    except Exception as e:
        raise e
