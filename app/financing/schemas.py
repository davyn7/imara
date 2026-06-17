# app/financing/schemas.py

from pydantic import BaseModel
from datetime import date
from typing import Optional, List
from uuid import UUID

# TODO: Add schemas for Financing

class SAFEBase(BaseModel):
    pass

class TradeFinancingBase(BaseModel):
    pass

class EquityFinancingBase(BaseModel):
    pass

class DebtFinancingBase(BaseModel):
    pass

class OtherFinancingBase(BaseModel):
    pass