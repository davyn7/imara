# app/internal/schemas.py

from pydantic import BaseModel
from datetime import date
from typing import Optional, List

# TODO: Add schemas for Internal

# Any Imara-owned company
class CompanyBase(BaseModel):
    name: Optional[str] = None
    legal_name: Optional[str] = None
    country: Optional[str] = None
    tax_id: Optional[str] = None
    registration_number: Optional[str] = None
    base_currency: Optional[str] = None
    address: Optional[str] = None
    zip_code: Optional[str] = None

# Any Imara-owned bank account
class AccountBase(BaseModel):
    company_id: Optional[int] = None
    name: Optional[str] = None
    bank_name: Optional[str] = None
    account_number: Optional[str] = None
    currency: Optional[str] = None
    country: Optional[str] = None
    swift_code: Optional[str] = None
    bank_address: Optional[str] = None
    opening_balance: Optional[float] = None
    current_balance: Optional[float] = None
    notes: Optional[str] = None

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

class ExpenseBase(BaseModel):
    account_id: Optional[int] = None
    name: Optional[str] = None
    category: Optional[str] = None
    amount: Optional[float] = None
    expense_date: Optional[date] = None
    description: Optional[str] = None
    notes: Optional[str] = None
    is_reimbursement: Optional[bool] = False

class ReimbursementBase(BaseModel):
    expense_id: Optional[int] = None
    user_id: Optional[int] = None
    is_reimbursed: Optional[bool] = False
    reimbursement_date: Optional[date] = None
    notes: Optional[str] = None