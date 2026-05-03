# app/router.py

from fastapi import APIRouter
from app.managers import (
    ActivityLogManager,
    CompanyManager,
    CounterpartyManager,
    TradeManager,
    TradeCostManager,
    BrokerageDealManager,
    ShipmentManager,
    ShareholderManager,
    EquityRoundManager,
    ShareTransactionManager
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

@router.post("/populate", tags=["Testing"])
async def populate():
    pass

@router.delete("/clear", tags=["Testing"])
async def clear():
    pass

# Company Routers

@router.get("/companies", tags=["Companies"])
async def get_companies():
    try:
        manager = CompanyManager(None)
        return await manager.get_companies()
    except Exception as e:
        raise e

@router.get("/companies/{company_id}", tags=["Companies"])
async def get_company(company_id: UUID):
    try:
        manager = CompanyManager(None)
        return await manager.get_company(company_id)
    except Exception as e:
        raise e

@router.post("/add_company", tags=["Companies"])
async def add_company(company: CompanyBase):
    try:
        manager = CompanyManager(company)
        return await manager.add_company()
    except Exception as e:
        raise e

@router.put("/update_company/{company_id}", tags=["Companies"])
async def update_company(company_id: UUID, company: CompanyBase):
    try:
        manager = CompanyManager(company)
        return await manager.update_company(company_id)
    except Exception as e:
        raise e

@router.delete("/delete_company/{company_id}", tags=["Companies"])
async def delete_company(company_id: UUID):
    try:
        manager = CompanyManager(None)
        return await manager.delete_company(company_id)
    except Exception as e:
        raise e

@router.delete("/delete_companies", tags=["Companies"])
async def delete_companies():
    try:
        manager = CompanyManager(None)
        return await manager.delete_companies()
    except Exception as e:
        raise e

# Counterparty Routers

@router.get("/counterparties", tags=["Counterparties"])
async def get_counterparties():
    try:
        manager = CounterpartyManager(None)
        return await manager.get_counterparties()
    except Exception as e:
        raise e

@router.get("/counterparties/{counterparty_id}", tags=["Counterparties"])
async def get_counterparty(counterparty_id: UUID):
    try:
        manager = CounterpartyManager(None)
        return await manager.get_counterparty(counterparty_id)
    except Exception as e:
        raise e

@router.post("/add_counterparty", tags=["Counterparties"])
async def add_counterparty(counterparty: CounterpartyBase):
    try:
        manager = CounterpartyManager(counterparty)
        return await manager.add_counterparty()
    except Exception as e:
        raise e

@router.put("/update_counterparty/{counterparty_id}", tags=["Counterparties"])
async def update_counterparty(counterparty_id: UUID, counterparty: CounterpartyBase):
    try:
        manager = CounterpartyManager(counterparty)
        return await manager.update_counterparty(counterparty_id)
    except Exception as e:
        raise e

@router.delete("/delete_counterparty/{counterparty_id}", tags=["Counterparties"])
async def delete_counterparty(counterparty_id: UUID):
    try:
        manager = CounterpartyManager(None)
        return await manager.delete_counterparty(counterparty_id)
    except Exception as e:
        raise e

@router.delete("/delete_counterparties", tags=["Counterparties"])
async def delete_counterparties():
    try:
        manager = CounterpartyManager(None)
        return await manager.delete_counterparties()
    except Exception as e:
        raise e

# Shareholder Routers

@router.get("/shareholders", tags=["Shareholders"])
async def get_shareholders():
    try:
        manager = ShareholderManager(None)
        return await manager.get_shareholders()
    except Exception as e:
        raise e

@router.get("/shareholders/{shareholder_id}", tags=["Shareholders"])
async def get_shareholder(shareholder_id: UUID):
    try:
        manager = ShareholderManager(None)
        return await manager.get_shareholder(shareholder_id)
    except Exception as e:
        raise e

@router.post("/add_shareholder", tags=["Shareholders"])
async def add_shareholder(shareholder: ShareholderBase):
    try:
        manager = ShareholderManager(shareholder)
        return await manager.add_shareholder()
    except Exception as e:
        raise e

@router.put("/update_shareholder/{shareholder_id}", tags=["Shareholders"])
async def update_shareholder(shareholder_id: UUID, shareholder: ShareholderBase):
    try:
        manager = ShareholderManager(shareholder)
        return await manager.update_shareholder(shareholder_id)
    except Exception as e:
        raise e

@router.delete("/delete_shareholder/{shareholder_id}", tags=["Shareholders"])
async def delete_shareholder(shareholder_id: UUID):
    try:
        manager = ShareholderManager(None)
        return await manager.delete_shareholder(shareholder_id)
    except Exception as e:
        raise e

@router.delete("/delete_shareholdes", tags=["Shareholders"])
async def delete_shareholder():
    try:
        manager = ShareholderManager(None)
        return await manager.delete_shareholders()
    except Exception as e:
        raise e

# Equity Round Routers

@router.get("/equity_rounds", tags=["Equity Rounds"])
async def get_equity_rounds():
    try:
        manager = EquityRoundManager(None)
        return await manager.get_equity_rounds()
    except Exception as e:
        raise e

@router.get("/equity_rounds/{equity_round_id}", tags=["Equity Rounds"])
async def get_equity_round(equity_round_id: UUID):
    try:
        manager = EquityRoundManager(None)
        return await manager.get_equity_round(equity_round_id)
    except Exception as e:
        raise e

@router.post("/add_equity_round", tags=["Equity Rounds"])
async def add_equity_round(equity_round: EquityRoundBase):
    try:
        manager = EquityRoundManager(equity_round)
        return await manager.add_equity_round()
    except Exception as e:
        raise e

@router.put("/update_equity_round/{equity_round_id}", tags=["Equity Rounds"])
async def update_equity_round(equity_round_id: UUID, equity_round: EquityRoundBase):
    try:
        manager = EquityRoundManager(equity_round)
        return await manager.update_equity_round(equity_round_id)
    except Exception as e:
        raise e

@router.delete("/delete_equity_round/{equity_round_id}", tags=["Equity Rounds"])
async def delete_equity_round(equity_round_id: UUID):
    try:
        manager = EquityRoundManager(None)
        return await manager.delete_equity_round(equity_round_id)
    except Exception as e:
        raise e

@router.delete("/delete_equity_rounds", tags=["Equity Rounds"])
async def delete_equity_rounds():
    try:
        manager = EquityRoundManager(None)
        return await manager.delete_equity_rounds()
    except Exception as e:
        raise e
