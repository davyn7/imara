# app/counterparties/schemas.py

from datetime import date, datetime
from decimal import Decimal
from enum import Enum
from typing import Optional, List

from pydantic import BaseModel


class CounterpartyType(str, Enum):
    COMPANY = "Company"
    INDIVIDUAL = "Individual"


class CounterpartyRole(str, Enum):
    SELLER = "Seller"
    BUYER = "Buyer"
    SURVEYOR = "Surveyor"
    LOGISTICS = "Logistics"
    PROVIDER = "Provider"
    BROKER = "Broker"
    AGENT = "Agent"
    FINANCIER = "Financier"
    INSURER = "Insurer"
    OTHER = "Other"


class CounterpartyStatus(str, Enum):
    ACTIVE = "Active"
    INACTIVE = "Inactive"
    BLACKLISTED = "Blacklisted"
    PROSPECTIVE = "Prospective"


class KYCStatus(str, Enum):
    NOT_STARTED = "Not Started"
    IN_PROGRESS = "In Progress"
    APPROVED = "Approved"
    REJECTED = "Rejected"
    EXPIRED = "Expired"


class ContractStatus(str, Enum):
    DRAFT = "Draft"
    UNDER_REVIEW = "Under Review"
    ACTIVE = "Active"
    EXPIRED = "Expired"
    TERMINATED = "Terminated"


class SPADirection(str, Enum):
    PURCHASE = "Purchase"  # We buy from counterparty
    SALE = "Sale"          # We sell to counterparty


class PaymentTerms(str, Enum):
    PREPAID = "Prepaid"
    CASH_AGAINST_DOCUMENTS = "Cash Against Documents"
    CASH_ON_DELIVERY = "Cash on Delivery"
    NET_7 = "Net 7"
    NET_14 = "Net 14"
    NET_30 = "Net 30"
    NET_60 = "Net 60"
    CUSTOM = "Custom"


class CounterpartyBase(BaseModel):
    company_id: Optional[int] = None

    name: Optional[str] = None
    counterparty_type: Optional[CounterpartyType] = None
    roles: Optional[List[CounterpartyRole]] = None
    status: Optional[CounterpartyStatus] = CounterpartyStatus.ACTIVE

    country: Optional[str] = None
    city: Optional[str] = None
    address: Optional[str] = None

    tax_id: Optional[str] = None
    registration_number: Optional[str] = None

    website: Optional[str] = None
    notes: Optional[str] = None


class CounterpartyCreate(CounterpartyBase):
    pass


class CounterpartyUpdate(CounterpartyBase):
    pass


class CounterpartyResponse(CounterpartyBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class CounterpartyContactBase(BaseModel):
    counterparty_id: Optional[int] = None

    name: Optional[str] = None
    title: Optional[str] = None
    department: Optional[str] = None

    email: Optional[str] = None
    phone: Optional[str] = None
    whatsapp: Optional[str] = None

    is_primary: Optional[bool] = False
    notes: Optional[str] = None


class CounterpartyContactCreate(CounterpartyContactBase):
    pass


class CounterpartyContactUpdate(CounterpartyContactBase):
    pass


class CounterpartyContactResponse(CounterpartyContactBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class CounterpartyBankAccountBase(BaseModel):
    counterparty_id: Optional[int] = None

    bank_name: Optional[str] = None
    account_name: Optional[str] = None
    account_number: Optional[str] = None
    currency: Optional[str] = None

    country: Optional[str] = None
    swift_code: Optional[str] = None
    bank_address: Optional[str] = None

    is_primary: Optional[bool] = False
    notes: Optional[str] = None


class CounterpartyBankAccountCreate(CounterpartyBankAccountBase):
    pass


class CounterpartyBankAccountUpdate(CounterpartyBankAccountBase):
    pass


class CounterpartyBankAccountResponse(CounterpartyBankAccountBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class CounterpartyKYCBase(BaseModel):
    counterparty_id: Optional[int] = None

    kyc_status: Optional[KYCStatus] = KYCStatus.NOT_STARTED
    reviewed_by: Optional[str] = None
    reviewed_at: Optional[datetime] = None

    document_url: Optional[str] = None
    expiry_date: Optional[date] = None

    risk_rating: Optional[str] = None
    notes: Optional[str] = None


class CounterpartyKYCCreate(CounterpartyKYCBase):
    pass


class CounterpartyKYCUpdate(CounterpartyKYCBase):
    pass


class CounterpartyKYCResponse(CounterpartyKYCBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class CounterpartySPABase(BaseModel):
    company_id: Optional[int] = None
    counterparty_id: Optional[int] = None

    spa_number: Optional[str] = None
    direction: Optional[SPADirection] = None
    status: Optional[ContractStatus] = ContractStatus.DRAFT

    commodity: Optional[str] = None
    product_specification: Optional[str] = None

    quantity: Optional[Decimal] = None
    quantity_unit: Optional[str] = None

    price: Optional[Decimal] = None
    price_currency: Optional[str] = None
    price_unit: Optional[str] = None

    payment_terms: Optional[PaymentTerms] = None
    custom_payment_terms: Optional[str] = None

    incoterm: Optional[str] = None
    loading_port: Optional[str] = None
    discharge_port: Optional[str] = None

    effective_date: Optional[date] = None
    expiry_date: Optional[date] = None
    signed_date: Optional[date] = None

    document_url: Optional[str] = None
    notes: Optional[str] = None


class CounterpartySPACreate(CounterpartySPABase):
    pass


class CounterpartySPAUpdate(CounterpartySPABase):
    pass


class CounterpartySPAResponse(CounterpartySPABase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class CounterpartyDocumentBase(BaseModel):
    counterparty_id: Optional[int] = None
    spa_id: Optional[int] = None

    name: Optional[str] = None
    document_type: Optional[str] = None
    document_url: Optional[str] = None

    issue_date: Optional[date] = None
    expiry_date: Optional[date] = None

    notes: Optional[str] = None


class CounterpartyDocumentCreate(CounterpartyDocumentBase):
    pass


class CounterpartyDocumentUpdate(CounterpartyDocumentBase):
    pass


class CounterpartyDocumentResponse(CounterpartyDocumentBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# from pydantic import BaseModel
# from datetime import date
# from typing import Optional, List
# from uuid import UUID

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