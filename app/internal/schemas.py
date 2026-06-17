# app/internal/schemas.py

from pydantic import BaseModel
from typing import Optional
from datetime import date

class CompanyBase(BaseModel):
    name: Optional[str] = None
    legal_name: Optional[str] = None
    country: Optional[str] = None
    tax_id: Optional[str] = None
    registration_number: Optional[str] = None
    base_currency: Optional[str] = None
    address: Optional[str] = None
    zip_code: Optional[str] = None

# class PersonBase(BaseModel):
#     first_name: Optional[str] = None
#     last_name: Optional[str] = None
#     full_name: Optional[str] = None
#     nationality: Optional[str] = None
#     tax_id: Optional[str] = None
#     id_number: Optional[str] = None
#     address: Optional[str] = None
#     zip_code: Optional[str] = None

# class ShareholdingBase(BaseModel):
#     company_id: Optional[int] = None
#     shareholder_type: Optional[str] = None # "person" or "company"
#     shareholder_person_id: Optional[int] = None
#     shareholder_company_id: Optional[int] = None
#     ownership_percentage: Optional[float] = None
#     share_class: Optional[str] = None
#     effective_from: Optional[date] = None
#     notes: Optional[str] = None
