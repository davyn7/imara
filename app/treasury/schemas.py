# app/treasury/schemas.py

from pydantic import BaseModel
from typing import Optional
from decimal import Decimal
from datetime import date, datetime
from enum import Enum


class AccountType(str, Enum):
    BANK = "bank"
    CASH = "cash"
    ESCROW = "escrow"
    BROKERAGE = "brokerage"
    OTHER = "other"


class TransactionType(str, Enum):
    INFLOW = "inflow"
    OUTFLOW = "outflow"
    TRANSFER = "transfer"
    FX_CONVERSION = "fx_conversion"
    ADJUSTMENT = "adjustment"


class TransactionCategory(str, Enum):
    TRADE_PURCHASE_PAYMENT = "trade_purchase_payment"
    TRADE_SALE_RECEIPT = "trade_sale_receipt"
    FREIGHT_PAYMENT = "freight_payment"
    INSURANCE_PAYMENT = "insurance_payment"
    SURVEY_PAYMENT = "survey_payment"
    FINANCING_DRAWDOWN = "financing_drawdown"
    FINANCING_REPAYMENT = "financing_repayment"
    INTEREST_PAYMENT = "interest_payment"
    BANK_FEE = "bank_fee"
    FX_CONVERSION = "fx_conversion"
    INTERNAL_TRANSFER = "internal_transfer"
    OPERATING_EXPENSE = "operating_expense"
    REIMBURSEMENT = "reimbursement"
    TAX = "tax"
    OTHER = "other"


class TransactionStatus(str, Enum):
    DRAFT = "draft"
    SCHEDULED = "scheduled"
    PENDING = "pending"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    FAILED = "failed"
    RECONCILED = "reconciled"


class PayableStatus(str, Enum):
    DRAFT = "draft"
    APPROVED = "approved"
    SCHEDULED = "scheduled"
    PARTIALLY_PAID = "partially_paid"
    PAID = "paid"
    OVERDUE = "overdue"
    CANCELLED = "cancelled"


class ReceivableStatus(str, Enum):
    DRAFT = "draft"
    INVOICED = "invoiced"
    PARTIALLY_RECEIVED = "partially_received"
    RECEIVED = "received"
    OVERDUE = "overdue"
    CANCELLED = "cancelled"


class TransferStatus(str, Enum):
    DRAFT = "draft"
    SCHEDULED = "scheduled"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    FAILED = "failed"


class ExpenseStatus(str, Enum):
    DRAFT = "draft"
    SUBMITTED = "submitted"
    APPROVED = "approved"
    REJECTED = "rejected"
    PAID = "paid"
    CANCELLED = "cancelled"


class ReimbursementStatus(str, Enum):
    SUBMITTED = "submitted"
    APPROVED = "approved"
    REJECTED = "rejected"
    SCHEDULED = "scheduled"
    REIMBURSED = "reimbursed"
    CANCELLED = "cancelled"


class AccountBase(BaseModel):
    company_id: Optional[int] = None

    name: Optional[str] = None
    account_type: Optional[AccountType] = AccountType.BANK

    bank_name: Optional[str] = None
    account_holder_name: Optional[str] = None
    account_number: Optional[str] = None

    currency: Optional[str] = None
    country: Optional[str] = None

    swift_code: Optional[str] = None
    iban: Optional[str] = None

    branch_name: Optional[str] = None
    bank_address: Optional[str] = None

    opening_balance: Optional[Decimal] = None
    current_balance: Optional[Decimal] = None
    opening_balance_date: Optional[date] = None

    is_active: Optional[bool] = True
    notes: Optional[str] = None


class TreasuryTransactionBase(BaseModel):
    account_id: int

    transaction_type: TransactionType
    category: Optional[TransactionCategory] = None
    status: Optional[TransactionStatus] = TransactionStatus.DRAFT

    amount: Decimal
    currency: str

    transaction_date: Optional[date] = None
    value_date: Optional[date] = None

    counterparty_id: Optional[int] = None
    trade_id: Optional[int] = None
    shipment_id: Optional[int] = None
    financing_id: Optional[int] = None
    expense_id: Optional[int] = None
    reimbursement_id: Optional[int] = None

    reference_number: Optional[str] = None
    description: Optional[str] = None
    notes: Optional[str] = None

    created_by_user_id: Optional[int] = None


class PayableBase(BaseModel):
    company_id: Optional[int] = None
    counterparty_id: Optional[int] = None

    trade_id: Optional[int] = None
    shipment_id: Optional[int] = None
    financing_id: Optional[int] = None
    expense_id: Optional[int] = None

    status: Optional[PayableStatus] = PayableStatus.DRAFT

    category: Optional[str] = None

    amount: Decimal
    currency: str

    due_date: Optional[date] = None
    invoice_date: Optional[date] = None
    invoice_number: Optional[str] = None

    amount_paid: Optional[Decimal] = Decimal("0")
    remaining_amount: Optional[Decimal] = None

    description: Optional[str] = None
    notes: Optional[str] = None


class ReceivableBase(BaseModel):
    company_id: Optional[int] = None
    counterparty_id: Optional[int] = None

    trade_id: Optional[int] = None
    shipment_id: Optional[int] = None
    financing_id: Optional[int] = None

    status: Optional[ReceivableStatus] = ReceivableStatus.DRAFT

    category: Optional[str] = None

    amount: Decimal
    currency: str

    due_date: Optional[date] = None
    invoice_date: Optional[date] = None
    invoice_number: Optional[str] = None

    amount_received: Optional[Decimal] = Decimal("0")
    remaining_amount: Optional[Decimal] = None

    description: Optional[str] = None
    notes: Optional[str] = None


class AccountTransferBase(BaseModel):
    from_account_id: int
    to_account_id: int

    amount: Decimal
    currency: str

    transfer_date: Optional[date] = None
    value_date: Optional[date] = None

    status: Optional[TransferStatus] = TransferStatus.DRAFT

    reference_number: Optional[str] = None
    notes: Optional[str] = None


class ExpenseBase(BaseModel):
    account_id: Optional[int] = None
    company_id: Optional[int] = None

    submitted_by_user_id: Optional[int] = None

    trade_id: Optional[int] = None
    shipment_id: Optional[int] = None

    name: Optional[str] = None
    category: Optional[str] = None
    status: Optional[ExpenseStatus] = ExpenseStatus.DRAFT

    amount: Optional[Decimal] = None
    currency: Optional[str] = None

    expense_date: Optional[date] = None

    description: Optional[str] = None
    notes: Optional[str] = None

    is_reimbursement: Optional[bool] = False


class ReimbursementBase(BaseModel):
    expense_id: Optional[int] = None
    user_id: Optional[int] = None

    status: Optional[ReimbursementStatus] = ReimbursementStatus.SUBMITTED

    amount: Optional[Decimal] = None
    currency: Optional[str] = None

    approved_by_user_id: Optional[int] = None
    reimbursed_from_account_id: Optional[int] = None
    treasury_transaction_id: Optional[int] = None

    reimbursement_date: Optional[date] = None

    notes: Optional[str] = None


class FxTransactionStatus(str, Enum):
    DRAFT = "draft"
    BOOKED = "booked"
    SETTLED = "settled"
    CANCELLED = "cancelled"


class FxTransactionBase(BaseModel):
    from_account_id: int
    to_account_id: int

    from_currency: str
    to_currency: str
    from_amount: Decimal
    to_amount: Decimal
    exchange_rate: Optional[Decimal] = None

    status: Optional[FxTransactionStatus] = FxTransactionStatus.DRAFT

    trade_date: Optional[date] = None
    settlement_date: Optional[date] = None

    reference_number: Optional[str] = None
    notes: Optional[str] = None


class BankStatementLineBase(BaseModel):
    account_id: int

    transaction_date: Optional[date] = None
    value_date: Optional[date] = None

    amount: Decimal
    currency: str

    description: Optional[str] = None
    reference_number: Optional[str] = None

    is_matched: Optional[bool] = False
    treasury_transaction_id: Optional[int] = None

    notes: Optional[str] = None


class ReconciliationStatus(str, Enum):
    OPEN = "open"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class ReconciliationBase(BaseModel):
    account_id: int

    reconciliation_date: Optional[date] = None
    opening_balance: Optional[Decimal] = None
    closing_balance: Optional[Decimal] = None

    status: Optional[ReconciliationStatus] = ReconciliationStatus.OPEN
    notes: Optional[str] = None


class ReconciliationMatchBase(BaseModel):
    treasury_transaction_id: int
    bank_statement_line_id: int
    reconciliation_id: Optional[int] = None


class CashBalanceSnapshotBase(BaseModel):
    account_id: int
    company_id: Optional[int] = None

    snapshot_date: Optional[date] = None
    balance: Decimal
    currency: str

    notes: Optional[str] = None
