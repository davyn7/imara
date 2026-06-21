# app/trades/schemas.py

from enum import Enum
from decimal import Decimal
from datetime import date, datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


# ============================================================
# Enums
# ============================================================

class TradeType(str, Enum):
    PHYSICAL = "physical"
    BACK_TO_BACK = "back_to_back"
    AGENCY = "agency"
    INDENT = "indent"
    OTHER = "other"


class TradeStatus(str, Enum):
    DRAFT = "draft"
    NEGOTIATION = "negotiation"
    CONTRACTED = "contracted"
    AWAITING_SHIPMENT = "awaiting_shipment"
    IN_TRANSIT = "in_transit"
    DELIVERED = "delivered"
    INVOICED = "invoiced"
    SETTLED = "settled"
    CLOSED = "closed"
    CANCELLED = "cancelled"
    DISPUTED = "disputed"


class TradeLegType(str, Enum):
    PURCHASE = "purchase"
    SALE = "sale"


class TradeLegStatus(str, Enum):
    DRAFT = "draft"
    CONTRACTED = "contracted"
    PARTIALLY_FULFILLED = "partially_fulfilled"
    FULFILLED = "fulfilled"
    CANCELLED = "cancelled"
    DISPUTED = "disputed"


class TradeCostCategory(str, Enum):
    ASSAY = "assay"
    INSURANCE = "insurance"
    SURVEY = "survey"
    FREIGHT = "freight"
    CUSTOMS = "customs"
    WAREHOUSING = "warehousing"
    DEMURRAGE = "demurrage"
    BANK_CHARGES = "bank_charges"
    BROKERAGE = "brokerage"
    FINANCING_COST = "financing_cost"
    TAX = "tax"
    OTHER = "other"


class TradeRevenueType(str, Enum):
    SALE_PROCEEDS = "sale_proceeds"
    QUALITY_ADJUSTMENT = "quality_adjustment"
    PRICE_ADJUSTMENT = "price_adjustment"
    CLAIM_RECOVERY = "claim_recovery"
    OTHER = "other"


class QuantityUnit(str, Enum):
    MT = "mt"
    WMT = "wmt"
    DMT = "dmt"
    KG = "kg"
    LB = "lb"
    UNIT = "unit"
    OTHER = "other"


class Incoterm(str, Enum):
    EXW = "exw"
    FCA = "fca"
    FAS = "fas"
    FOB = "fob"
    CFR = "cfr"
    CIF = "cif"
    CPT = "cpt"
    CIP = "cip"
    DAP = "dap"
    DPU = "dpu"
    DDP = "ddp"
    OTHER = "other"


# ============================================================
# Trade
# ============================================================

class TradeBase(BaseModel):
    trade_code: Optional[str] = None

    imara_entity_id: Optional[int] = None

    trade_type: Optional[TradeType] = TradeType.PHYSICAL
    status: Optional[TradeStatus] = TradeStatus.DRAFT

    commodity: Optional[str] = None

    seller_counterparty_id: Optional[int] = None
    buyer_counterparty_id: Optional[int] = None

    purchase_contract_number: Optional[str] = None
    sales_contract_number: Optional[str] = None

    purchase_date: Optional[date] = None
    sales_date: Optional[date] = None

    base_currency: Optional[str] = None

    notes: Optional[str] = None


class TradeCreate(TradeBase):
    pass


class TradeUpdate(BaseModel):
    trade_code: Optional[str] = None

    imara_entity_id: Optional[int] = None

    trade_type: Optional[TradeType] = None
    status: Optional[TradeStatus] = None

    commodity: Optional[str] = None

    seller_counterparty_id: Optional[int] = None
    buyer_counterparty_id: Optional[int] = None

    purchase_contract_number: Optional[str] = None
    sales_contract_number: Optional[str] = None

    purchase_date: Optional[date] = None
    sales_date: Optional[date] = None

    base_currency: Optional[str] = None

    notes: Optional[str] = None


class TradeRead(TradeBase):
    id: int


# ============================================================
# Trade Legs
# ============================================================

class TradeLegBase(BaseModel):
    trade_id: int

    leg_type: TradeLegType
    status: Optional[TradeLegStatus] = TradeLegStatus.DRAFT

    counterparty_id: int
    imara_entity_id: int

    contract_number: Optional[str] = None
    contract_date: Optional[date] = None

    incoterm: Optional[Incoterm] = None
    currency: Optional[str] = None

    quantity: Optional[Decimal] = None
    quantity_unit: Optional[QuantityUnit] = None

    unit_price: Optional[Decimal] = None
    total_price: Optional[Decimal] = None

    payment_terms: Optional[str] = None
    delivery_terms: Optional[str] = None

    notes: Optional[str] = None


class TradeLegCreate(TradeLegBase):
    pass


class TradeLegUpdate(BaseModel):
    status: Optional[TradeLegStatus] = None

    counterparty_id: Optional[int] = None
    imara_entity_id: Optional[int] = None

    contract_number: Optional[str] = None
    contract_date: Optional[date] = None

    incoterm: Optional[Incoterm] = None
    currency: Optional[str] = None

    quantity: Optional[Decimal] = None
    quantity_unit: Optional[QuantityUnit] = None

    unit_price: Optional[Decimal] = None
    total_price: Optional[Decimal] = None

    payment_terms: Optional[str] = None
    delivery_terms: Optional[str] = None

    notes: Optional[str] = None


class TradeLegRead(TradeLegBase):
    id: int


# ============================================================
# Trade Items / Commodities
# ============================================================

class TradeItemBase(BaseModel):
    trade_id: int

    commodity: str
    grade: Optional[str] = None
    specification: Optional[str] = None

    quantity: Decimal
    quantity_unit: QuantityUnit

    expected_quality: Optional[str] = None
    actual_quality: Optional[str] = None

    notes: Optional[str] = None


class TradeItemCreate(TradeItemBase):
    pass


class TradeItemUpdate(BaseModel):
    commodity: Optional[str] = None
    grade: Optional[str] = None
    specification: Optional[str] = None

    quantity: Optional[Decimal] = None
    quantity_unit: Optional[QuantityUnit] = None

    expected_quality: Optional[str] = None
    actual_quality: Optional[str] = None

    notes: Optional[str] = None


class TradeItemRead(TradeItemBase):
    id: int


# ============================================================
# Trade Costs
# ============================================================

class TradeCostBase(BaseModel):
    trade_id: int

    category: TradeCostCategory
    description: Optional[str] = None

    counterparty_id: Optional[int] = None

    amount: Decimal
    currency: str

    exchange_rate_to_base: Optional[Decimal] = None
    amount_base_currency: Optional[Decimal] = None

    cost_date: Optional[date] = None
    due_date: Optional[date] = None
    paid_date: Optional[date] = None

    is_estimated: bool = True
    is_pass_through: bool = False

    notes: Optional[str] = None


class TradeCostCreate(TradeCostBase):
    pass


class TradeCostUpdate(BaseModel):
    category: Optional[TradeCostCategory] = None
    description: Optional[str] = None

    counterparty_id: Optional[int] = None

    amount: Optional[Decimal] = None
    currency: Optional[str] = None

    exchange_rate_to_base: Optional[Decimal] = None
    amount_base_currency: Optional[Decimal] = None

    cost_date: Optional[date] = None
    due_date: Optional[date] = None
    paid_date: Optional[date] = None

    is_estimated: Optional[bool] = None
    is_pass_through: Optional[bool] = None

    notes: Optional[str] = None


class TradeCostRead(TradeCostBase):
    id: int


# ============================================================
# Trade Revenues
# ============================================================

class TradeRevenueBase(BaseModel):
    trade_id: int

    revenue_type: TradeRevenueType
    description: Optional[str] = None

    counterparty_id: Optional[int] = None

    amount: Decimal
    currency: str

    exchange_rate_to_base: Optional[Decimal] = None
    amount_base_currency: Optional[Decimal] = None

    revenue_date: Optional[date] = None

    is_estimated: bool = True

    notes: Optional[str] = None


class TradeRevenueCreate(TradeRevenueBase):
    pass


class TradeRevenueUpdate(BaseModel):
    revenue_type: Optional[TradeRevenueType] = None
    description: Optional[str] = None

    counterparty_id: Optional[int] = None

    amount: Optional[Decimal] = None
    currency: Optional[str] = None

    exchange_rate_to_base: Optional[Decimal] = None
    amount_base_currency: Optional[Decimal] = None

    revenue_date: Optional[date] = None

    is_estimated: Optional[bool] = None

    notes: Optional[str] = None


class TradeRevenueRead(TradeRevenueBase):
    id: int


# ============================================================
# Trade Status Events
# ============================================================

class TradeStatusEventBase(BaseModel):
    trade_id: int

    status: TradeStatus
    changed_at: Optional[datetime] = None
    changed_by_user_id: Optional[int] = None

    notes: Optional[str] = None


class TradeStatusEventCreate(TradeStatusEventBase):
    pass


class TradeStatusEventUpdate(BaseModel):
    status: Optional[TradeStatus] = None
    changed_at: Optional[datetime] = None
    changed_by_user_id: Optional[int] = None
    notes: Optional[str] = None


class TradeStatusEventRead(TradeStatusEventBase):
    id: int


# ============================================================
# Trade Notes
# ============================================================

class TradeNoteBase(BaseModel):
    trade_id: int

    note: str
    created_by_user_id: Optional[int] = None
    created_at: Optional[datetime] = None


class TradeNoteCreate(TradeNoteBase):
    pass


class TradeNoteUpdate(BaseModel):
    note: Optional[str] = None


class TradeNoteRead(TradeNoteBase):
    id: int


# ============================================================
# Trade Margin Summary
# ============================================================

class TradeMarginSummary(BaseModel):
    trade_id: int
    base_currency: str

    estimated_revenue: Decimal
    estimated_purchase_cost: Decimal
    estimated_trade_costs: Decimal
    estimated_gross_profit: Decimal
    estimated_margin_percentage: Optional[Decimal] = None

    actual_revenue: Optional[Decimal] = None
    actual_purchase_cost: Optional[Decimal] = None
    actual_trade_costs: Optional[Decimal] = None
    actual_gross_profit: Optional[Decimal] = None
    actual_margin_percentage: Optional[Decimal] = None
