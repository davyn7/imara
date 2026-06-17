# app/treasury/schemas.py

from pydantic import BaseModel
from datetime import date
from typing import Optional

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
