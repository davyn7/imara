# app/schemas.py

from pydantic import BaseModel
from datetime import date
from typing import Optional, List
from uuid import UUID

# Activity Log Schema

class ActivityLogBase(BaseModel):
    # user_id: Optional[UUID] = None
    entity_type: Optional[str] = None
    entity_id: Optional[UUID] = None
    action: Optional[str] = None
    # old_data: Optional[dict] = None
    # new_data: Optional[dict] = None

# Company Schema

class CompanyBase(BaseModel):
    name: Optional[str] = None
    legal_name: Optional[str] = None
    country: Optional[str] = None
    tax_id: Optional[str] = None
    registration_number: Optional[str] = None
    base_currency: Optional[str] = None

# Bank Account Schema

class BankAccountBase(BaseModel):
    company_id: Optional[UUID] = None
    bank_name: Optional[str] = None
    account_name: Optional[str] = None
    account_number: Optional[str] = None
    currency: Optional[str] = None
    country: Optional[str] = None
    opening_balance: Optional[float] = None
    current_balance: Optional[float] = None
    notes: Optional[str] = None

# Counterparty Schema

class CounterpartyBase(BaseModel):
    counterparty_code: Optional[str] = None
    name: Optional[str] = None
    counterparty_type: Optional[str] = "other" # 'buyer', 'seller', 'broker', 'logistics_provider', 'lab', 'bank', 'insurer', 'financier', 'investor', 'other'
    country: Optional[str] = None
    city: Optional[str] = None
    contact_person: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    website: Optional[str] = None
    kyc_status: Optional[str] = "not_started" # 'not_started', 'in_progress', 'approved', 'rejected', 'expired'
    risk_rating: Optional[str] = "low" # 'low', 'medium', 'high', 'blacklisted'
    credit_limit: Optional[float] = None
    default_currency: Optional[str] = None
    notes: Optional[str] = None

# Trade Schema

class TradeBase(BaseModel):
    company_id: Optional[UUID] = None
    trade_code: Optional[str] = None
    commodity: Optional[str] = None
    product_form: Optional[str] = None
    grade_spec: Optional[str] = None
    quantity: Optional[int] = None
    unit: Optional[str] = None
    seller_id: Optional[UUID] = None
    buyer_id: Optional[UUID] = None
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
    # created_by: Optional[UUID] = None
    # created_at: Optional[date] = None
    # updated_at: Optional[date] = None

# Trade Cost Schema

class TradeCostBase(BaseModel):
    trade_id: Optional[UUID] = None
    cost_type: Optional[str] = "miscellaneous" # 'freight', 'insurance', 'assay', 'customs', 'warehouse', 'port_charges', 'trucking', 'financing', 'legal', 'brokerage', 'tax', 'inspection', 'miscellaneous'
    vendor_id: Optional[UUID] = None
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

# Brokerage Deal Schema

class BrokerageDealBase(BaseModel):
    company_id: Optional[UUID] = None
    deal_code: Optional[str] = None
    commodity: Optional[str] = None
    product_form: Optional[str] = None
    grade_spec: Optional[str] = None
    quantity: Optional[int] = None
    unit: Optional[str] = None
    seller_id: Optional[UUID] = None
    buyer_id: Optional[UUID] = None
    origin_country: Optional[str] = None
    origin_location: Optional[str] = None
    destination_country: Optional[str] = None
    destination_location: Optional[str] = None
    contract_value: Optional[float] = None
    currency: Optional[str] = None
    commission_type: Optional[str] = None
    commission_rate: Optional[float] = None
    commission_amount: Optional[float] = None
    payment_trigger: Optional[str] = None
    status: Optional[str] = "lead" # 'lead', 'negotiation', 'mandate_signed', 'contracted', 'completed', 'commission_invoiced', 'commission_paid', 'cancelled', 'disputed'
    trade_date: Optional[date] = None
    expected_commission_date: Optional[date] = None
    notes: Optional[str] = None
    # created_by: Optional[UUID] = None
    # created_at: Optional[date] = None
    # updated_at: Optional[date] = None

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

# Equity Round Schema

class EquityRoundBase(BaseModel):
    company_id: Optional[UUID] = None
    round_name: Optional[str] = None
    closing_date: Optional[date] = None
    pre_money_valuation: Optional[int] = None
    post_money_valuation: Optional[int] = None
    currency: Optional[str] = None
    total_raised: Optional[int] = None
    notes: Optional[str] = None

# Shareholder Schema

class ShareholderBase(BaseModel):
    company_id: Optional[UUID] = None
    shareholder_name: Optional[str] = None
    shareholder_type: Optional[str] = "other" # 'founder', 'individual_investor', 'corporate_investor', 'employee', 'advisor', 'other'
    email: Optional[str] = None
    country: Optional[str] = None
    account_name: Optional[str] = None
    account_number: Optional[str] = None
    bank_name: Optional[str] = None
    bank_swift: Optional[str] = None
    bank_address: Optional[str] = None
    shares: Optional[int] = None
    notes: Optional[str] = None

# Share Transaction Schema

class ShareTransactionBase(BaseModel):
    company_id: Optional[UUID] = None
    shareholder_id: Optional[UUID] = None
    equity_round_id: Optional[UUID] = None
    transaction_type: Optional[str] = "other" # 'issuance', 'transfer_in', 'transfer_out', 'buyback', 'conversion', 'option_grant', 'option_exercise', 'other'
    transaction_date: Optional[date] = None
    shares: Optional[int] = None
    price_per_share: Optional[float] = None
    investment_amount: Optional[int] = None
    currency: Optional[str] = None
    notes: Optional[str] = None
