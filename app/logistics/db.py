# app/logistics/db.py

from app.connection import supabase
from app.logistics.schemas import ShipmentBase

# Shipment DB Operations

async def get_shipments_db():
    response = supabase.table("shipments").select("*").execute()
    return response.data

async def get_shipment_db(shipment_id: int):
    response = supabase.table("shipments").select("*").eq("id", shipment_id).execute()
    return response.data

async def add_shipment_db(shipment: ShipmentBase):
    shipment_data = shipment.model_dump(mode="json")
    response = supabase.table("shipments").insert(shipment_data).execute()
    return response.data

async def update_shipment_db(shipment: ShipmentBase, shipment_id: int):
    shipment_data = shipment.model_dump(mode="json", exclude_unset=True)
    response = supabase.table("shipments").update(shipment_data).eq("id", shipment_id).execute()
    return response.data

async def delete_shipment_db(shipment_id: int):
    response = supabase.table("shipments").delete().eq("id", shipment_id).execute()
    return response.data

async def delete_shipments_db():
    response = supabase.table("shipments").delete().neq("id", 0).execute()
    return response.data
