# app/trades/schemas.py

from pydantic import BaseModel
from datetime import date
from typing import Optional, List
from uuid import UUID

# TODO: Add schemas for Trades

class TradeBase(BaseModel):
    company_id: Optional[int] = None
    trade_code: Optional[str] = None
    commodity: Optional[str] = None
    product_form: Optional[str] = None
    grade_spec: Optional[str] = None
    quantity: Optional[int] = None
    unit: Optional[str] = None
    seller_id: Optional[int] = None
    buyer_id: Optional[int] = None
    origin_country: Optional[str] = None
    origin_location: Optional[str] = None
    destination_country: Optional[str] = None
    destination_location: Optional[str] = None
    incoterm_purchase: Optional[str] = None
    incoterm_sale: Optional[str] = None
    trade_currency: Optional[str] = None
    purchase_price_per_unit: Optional[float] = None
    sale_price_per_unit: Optional[float] = None
    pruchase_pricing_formula: Optional[str] = None
    sale_pricing_formula: Optional[str] = None
    expected_purchase_value: Optional[float] = None
    expected_sale_value: Optional[float] = None
    status: Optional[str] = "draft" # 'draft', 'negotiation', 'contracted', 'in_transit', 'delivered', 'settled', 'cancelled', 'disputed'
    trade_date: Optional[date] = None
    expected_shipment_date: Optional[date] = None
    expected_delivery_date: Optional[date] = None
    expected_payment_date: Optional[date] = None
    notes: Optional[str] = None
    is_brokerage: Optional[bool] = False
    commission_on: Optional[str] = None # 'purchase', 'sale', 'both', 'margin
    commission: Optional[float] = None

# Trade Cost Schema

class TradeCostBase(BaseModel):
    trade_id: Optional[int] = None
    cost_type: Optional[str] = "miscellaneous" # 'freight', 'insurance', 'assay', 'customs', 'warehouse', 'port_charges', 'trucking', 'financing', 'legal', 'brokerage', 'tax', 'inspection', 'miscellaneous'
    vendor_id: Optional[int] = None
    description: Optional[str] = None
    amount: Optional[float] = None
    currency: Optional[str] = None
    fx_rate_to_trade_currency: Optional[float] = None
    amount_in_trade_currency: Optional[float] = None
    invoice_id: Optional[UUID] = None
    paid_status: Optional[str] = None
    cost_date: Optional[date] = None
    due_date: Optional[date] = None
    notes: Optional[str] = None

# Shipment Schema

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