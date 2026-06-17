# app/internal/schemas.py

from pydantic import BaseModel
from typing import Optional

class CompanyBase(BaseModel):
    name: Optional[str] = None
    legal_name: Optional[str] = None
    country: Optional[str] = None
    tax_id: Optional[str] = None
    registration_number: Optional[str] = None
    base_currency: Optional[str] = None
    address: Optional[str] = None
    zip_code: Optional[str] = None

class UserBase(BaseModel):
    company_id: Optional[int] = None
    name: Optional[str] = None
    personal_email: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    role: Optional[str] = None
    password: Optional[str] = None
    is_admin: Optional[bool] = False
    is_superadmin: Optional[bool] = False
    is_active: Optional[bool] = False
    notes: Optional[str] = None
