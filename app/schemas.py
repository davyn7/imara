# app/schemas.py

from pydantic import BaseModel
from datetime import date
from typing import Optional, List

# Company Schema

class CompanyBase(BaseModel):
    name: Optional[str] = None
    legal_name: Optional[str] = None
    country: Optional[str] = None
    tax_id: Optional[str] = None
    registration_number: Optional[str] = None
    base_currency: Optional[str] = None


