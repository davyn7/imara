# app/counterparties/schemas.py

from pydantic import BaseModel
from datetime import date
from typing import Optional, List
from uuid import UUID

# TODO: Add schemas for Counterparties

class CounterpartyBase(BaseModel):
    counterparty_code: Optional[str] = None
    name: Optional[str] = None
    counterparty_type: Optional[str] = None # 'buyer', 'seller', 'broker', 'logistics_provider', 'lab', 'bank', 'insurer', 'financier', 'investor', 'other'
    country: Optional[str] = None
    city: Optional[str] = None
    contact_person: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    website: Optional[str] = None
    notes: Optional[str] = None

class SPABase(BaseModel):
    counterparty_id: Optional[int] = None
    spa_code: Optional[str] = None
    spa_type: Optional[str] = "other" # 'buyer', 'seller', 'broker', 'logistics_provider', 'lab', 'bank', 'insurer', 'financier', 'investor', 'other'
    country: Optional[str] = None
    city: Optional[str] = None
    contact_person: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None