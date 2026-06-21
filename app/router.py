# app/router.py

from fastapi import APIRouter
from app.managers import (
    ActivityLogManager,
    CompanyManager,
    BankAccountManager,
    BrokerageDealManager,
    ShipmentManager,
    ShareholderManager,
    EquityRoundManager,
    ShareTransactionManager
)
from app.schemas import (
    ActivityLogBase,
    CompanyBase,
    BankAccountBase,
    BrokerageDealBase,
    ShipmentBase,
    EquityRoundBase,
    ShareholderBase,
    ShareTransactionBase
)
from uuid import UUID

router = APIRouter(prefix="/refactor", tags=["Refactor"])

# Initialize DB Testing

@router.post("/populate")
async def populate():
    pass

@router.delete("/clear")
async def clear():
    pass

# Company Routers

@router.get("/companies")
async def get_companies():
    try:
        manager = CompanyManager(None)
        return await manager.get_companies()
    except Exception as e:
        raise e

@router.get("/companies/{company_id}")
async def get_company(company_id: UUID):
    try:
        manager = CompanyManager(None)
        return await manager.get_company(company_id)
    except Exception as e:
        raise e

@router.post("/add_company")
async def add_company(company: CompanyBase):
    try:
        manager = CompanyManager(company)
        return await manager.add_company()
    except Exception as e:
        raise e

@router.put("/update_company/{company_id}")
async def update_company(company_id: UUID, company: CompanyBase):
    try:
        manager = CompanyManager(company)
        return await manager.update_company(company_id)
    except Exception as e:
        raise e

@router.delete("/delete_company/{company_id}")
async def delete_company(company_id: UUID):
    try:
        manager = CompanyManager(None)
        return await manager.delete_company(company_id)
    except Exception as e:
        raise e

@router.delete("/delete_companies")
async def delete_companies():
    try:
        manager = CompanyManager(None)
        return await manager.delete_companies()
    except Exception as e:
        raise e

# Bank Account Routers

@router.get("/bank_accounts")
async def get_bank_accounts():
    try:
        manager = BankAccountManager(None)
        return await manager.get_bank_accounts()
    except Exception as e:
        raise e

@router.get("/bank_accounts/{bank_account_id}")
async def get_bank_account(bank_account_id: UUID):
    try:
        manager = BankAccountManager(None)
        return await manager.get_bank_account(bank_account_id)
    except Exception as e:
        raise e

@router.post("/add_bank_account")
async def add_bank_account(bank_account: BankAccountBase):
    try:
        manager = BankAccountManager(bank_account)
        return await manager.add_bank_account()
    except Exception as e:
        raise e

@router.put("/update_bank_account/{bank_account_id}")
async def update_bank_account(bank_account_id: UUID, bank_account: BankAccountBase):
    try:
        manager = BankAccountManager(bank_account)
        return await manager.update_bank_account(bank_account_id)
    except Exception as e:
        raise e

@router.delete("/delete_bank_account/{bank_account_id}")
async def delete_bank_account(bank_account_id: UUID):
    try:
        manager = BankAccountManager(None)
        return await manager.delete_bank_account(bank_account_id)
    except Exception as e:
        raise e

@router.delete("/delete_bank_accounts")
async def delete_bank_accounts():
    try:
        manager = BankAccountManager(None)
        return await manager.delete_bank_accounts()
    except Exception as e:
        raise e

# Brokerage Deal Routers

@router.get("/brokerage_deals")
async def get_brokerage_deals():
    try:
        manager = BrokerageDealManager(None)
        return await manager.get_brokerage_deals()
    except Exception as e:
        raise e

@router.get("/brokerage_deals/{brokerage_deal_id}")
async def get_brokerage_deal(brokerage_deal_id: UUID):
    try:
        manager = BrokerageDealManager(None)
        return await manager.get_brokerage_deal(brokerage_deal_id)
    except Exception as e:
        raise e

@router.post("/add_brokerage_deal")
async def add_brokerage_deal(brokerage_deal: BrokerageDealBase):
    try:
        manager = BrokerageDealManager(brokerage_deal)
        return await manager.add_brokerage_deal()
    except Exception as e:
        raise e

@router.put("/update_brokerage_deal/{brokerage_deal_id}")
async def update_brokerage_deal(brokerage_deal_id: UUID, brokerage_deal: BrokerageDealBase):
    try:
        manager = BrokerageDealManager(brokerage_deal)
        return await manager.update_brokerage_deal(brokerage_deal_id)
    except Exception as e:
        raise e

@router.delete("/delete_brokerage_deal/{brokerage_deal_id}")
async def delete_brokerage_deal(brokerage_deal_id: UUID):
    try:
        manager = BrokerageDealManager(None)
        return await manager.delete_brokerage_deal(brokerage_deal_id)
    except Exception as e:
        raise e

@router.delete("/delete_brokerage_deals")
async def delete_brokerage_deals():
    try:
        manager = BrokerageDealManager(None)
        return await manager.delete_brokerage_deals()
    except Exception as e:
        raise e

# Shipment Routers

@router.get("/shipments")
async def get_shipments():
    try:
        manager = ShipmentManager(None)
        return await manager.get_shipments()
    except Exception as e:
        raise e

@router.get("/shipments/{shipment_id}")
async def get_shipment(shipment_id: UUID):
    try:
        manager = ShipmentManager(None)
        return await manager.get_shipment(shipment_id)
    except Exception as e:
        raise e

@router.post("/add_shipment")
async def add_shipment(shipment: ShipmentBase):
    try:
        manager = ShipmentManager(shipment)
        return await manager.add_shipment()
    except Exception as e:
        raise e

@router.put("/update_shipment/{shipment_id}")
async def update_shipment(shipment_id: UUID, shipment: ShipmentBase):
    try:
        manager = ShipmentManager(shipment)
        return await manager.update_shipment(shipment_id)
    except Exception as e:
        raise e

@router.delete("/delete_shipment/{shipment_id}")
async def delete_shipment(shipment_id: UUID):
    try:
        manager = ShipmentManager(None)
        return await manager.delete_shipment(shipment_id)
    except Exception as e:
        raise e

@router.delete("/delete_shipments")
async def delete_shipments():
    try:
        manager = ShipmentManager(None)
        return await manager.delete_shipments()
    except Exception as e:
        raise e

# Shareholder Routers

@router.get("/shareholders")
async def get_shareholders():
    try:
        manager = ShareholderManager(None)
        return await manager.get_shareholders()
    except Exception as e:
        raise e

@router.get("/shareholders/{shareholder_id}")
async def get_shareholder(shareholder_id: UUID):
    try:
        manager = ShareholderManager(None)
        return await manager.get_shareholder(shareholder_id)
    except Exception as e:
        raise e

@router.post("/add_shareholder")
async def add_shareholder(shareholder: ShareholderBase):
    try:
        manager = ShareholderManager(shareholder)
        return await manager.add_shareholder()
    except Exception as e:
        raise e

@router.put("/update_shareholder/{shareholder_id}")
async def update_shareholder(shareholder_id: UUID, shareholder: ShareholderBase):
    try:
        manager = ShareholderManager(shareholder)
        return await manager.update_shareholder(shareholder_id)
    except Exception as e:
        raise e

@router.delete("/delete_shareholder/{shareholder_id}")
async def delete_shareholder(shareholder_id: UUID):
    try:
        manager = ShareholderManager(None)
        return await manager.delete_shareholder(shareholder_id)
    except Exception as e:
        raise e

@router.delete("/delete_shareholdes")
async def delete_shareholder():
    try:
        manager = ShareholderManager(None)
        return await manager.delete_shareholders()
    except Exception as e:
        raise e

# Equity Round Routers

@router.get("/equity_rounds")
async def get_equity_rounds():
    try:
        manager = EquityRoundManager(None)
        return await manager.get_equity_rounds()
    except Exception as e:
        raise e

@router.get("/equity_rounds/{equity_round_id}")
async def get_equity_round(equity_round_id: UUID):
    try:
        manager = EquityRoundManager(None)
        return await manager.get_equity_round(equity_round_id)
    except Exception as e:
        raise e

@router.post("/add_equity_round")
async def add_equity_round(equity_round: EquityRoundBase):
    try:
        manager = EquityRoundManager(equity_round)
        return await manager.add_equity_round()
    except Exception as e:
        raise e

@router.put("/update_equity_round/{equity_round_id}")
async def update_equity_round(equity_round_id: UUID, equity_round: EquityRoundBase):
    try:
        manager = EquityRoundManager(equity_round)
        return await manager.update_equity_round(equity_round_id)
    except Exception as e:
        raise e

@router.delete("/delete_equity_round/{equity_round_id}")
async def delete_equity_round(equity_round_id: UUID):
    try:
        manager = EquityRoundManager(None)
        return await manager.delete_equity_round(equity_round_id)
    except Exception as e:
        raise e

@router.delete("/delete_equity_rounds")
async def delete_equity_rounds():
    try:
        manager = EquityRoundManager(None)
        return await manager.delete_equity_rounds()
    except Exception as e:
        raise e

# Share Transaction Routers

@router.get("/share_transactions")
async def get_share_transactions():
    try:
        manager = ShareTransactionManager(None)
        return await manager.get_share_transactions()
    except Exception as e:
        raise e

@router.get("/share_transactions/{share_transaction_id}")
async def get_share_transaction(share_transaction_id: UUID):
    try:
        manager = ShareTransactionManager(None)
        return await manager.get_share_transaction(share_transaction_id)
    except Exception as e:
        raise e

@router.post("/add_share_transaction")
async def add_share_transaction(share_transaction: ShareTransactionBase):
    try:
        manager = ShareTransactionManager(share_transaction)
        return await manager.add_share_transaction()
    except Exception as e:
        raise e

@router.put("/update_share_transaction/{share_transaction_id}")
async def update_share_transaction(share_transaction_id: UUID, share_transaction: ShareTransactionBase):
    try:
        manager = ShareTransactionManager(share_transaction)
        return await manager.update_share_transaction(share_transaction_id)
    except Exception as e:
        raise e

@router.delete("/delete_share_transaction/{share_transaction_id}")
async def delete_share_transaction(share_transaction_id: UUID):
    try:
        manager = ShareTransactionManager(None)
        return await manager.delete_share_transaction(share_transaction_id)
    except Exception as e:
        raise e

@router.delete("/delete_share_transactions")
async def delete_share_transactions():
    try:
        manager = ShareTransactionManager(None)
        return await manager.delete_share_transactions()
    except Exception as e:
        raise e