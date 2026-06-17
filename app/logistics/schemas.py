# app/logistics/schemas.py

from pydantic import BaseModel
from datetime import date
from typing import Optional
from uuid import UUID

class ShipmentBase(BaseModel):
    trade_id: Optional[UUID] = None
    shipment_code: Optional[str] = None
    mode: Optional[str] = None # 'air', 'sea', 'road', 'rail', 'multimodal'
    carrier_name: Optional[str] = None
    freight_forwarder_id: Optional[UUID] = None
    vessel_name: Optional[str] = None
    voyage_number: Optional[str] = None
    bl_number: Optional[str] = None
    container_numbers: Optional[str] = None
    origin_port: Optional[str] = None
    destination_port: Optional[str] = None
    eta: Optional[date] = None
    etd: Optional[date] = None
    actual_arrival_date: Optional[date] = None
    actual_departure_date: Optional[date] = None
    shipment_status: Optional[str] = "planned" # 'planned', 'booked', 'loaded', 'in_transit', 'arrived', 'customs_clearance', 'delivered', 'delayed', 'cancelled'
    notes: Optional[str] = None
