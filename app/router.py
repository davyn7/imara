# app/router.py

from fastapi import APIRouter
from app.managers import (
    CompanyManager,
    ShareholderManager
)
from app.schemas import (
    ActivityLogBase,
    CompanyBase,
    CounterpartyBase,
    TradeBase,
    TradeCostBase,
    BrokerageDealBase,
    ShipmentBase,
    EquityRoundBase,
    ShareholderBase,
    ShareTransactionBase
)
from uuid import UUID

router = APIRouter()

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

# @router.get("/trades")
# def list_trades():
#     return get_trades()


# @router.post("/trades")
# def add_trade(trade: dict):
#     return create_trade(trade)