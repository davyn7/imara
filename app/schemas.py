# app/schemas.py

from pydantic import BaseModel
from datetime import date
from typing import Optional, List
from uuid import UUID

# Activity Log Schema

class ActivityLogBase(BaseModel):
    # TODO: Update activity when a new action is done on DB.
    pass

# Company Schema

class CompanyBase(BaseModel):
    name: Optional[str] = None
    legal_name: Optional[str] = None
    country: Optional[str] = None
    tax_id: Optional[str] = None
    registration_number: Optional[str] = None
    base_currency: Optional[str] = None

# Counterparty Schema

class CounterpartyBase(BaseModel):
    # TODO
    pass

# Trade Schema

class TradeBase(BaseModel):
    # TODO
    pass

# Trade Cost Schema

class TradeCostBase(BaseModel):
    # TODO
    pass

# Brokerage Deal Schema

class BrokerageDealBase(BaseModel):
    # TODO
    pass

# Shipment Schema

class ShipmentBase(BaseModel):
    # TODO
    pass

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
    shareholder_type: Optional[str] = None
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
    transaction_type: Optional[str] = None
    transaction_date: Optional[date] = None
    shares: Optional[int] = None
    price_per_share: Optional[float] = None
    investment_amount: Optional[int] = None
    currency: Optional[str] = None
    notes: Optional[str] = None
