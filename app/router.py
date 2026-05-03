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

# Trade Routers

@router.get("/trades", tags=["Trades"])
async def get_trades():
    try:
        manager = TradeManager(None)
        return await manager.get_trades()
    except Exception as e:
        raise e

@router.get("/trades/{trade_id}", tags=["Trades"])
async def get_trade(trade_id: UUID):
    try:
        manager = TradeManager(None)
        return await manager.get_trade(trade_id)
    except Exception as e:
        raise e

@router.post("/add_trade", tags=["Trades"])
async def add_trade(trade: TradeBase):
    try:
        manager = TradeManager(trade)
        return await manager.add_trade()
    except Exception as e:
        raise e

@router.put("/update_trade/{trade_id}", tags=["Trades"])
async def update_trade(trade_id: UUID, trade: TradeBase):
    try:
        manager = TradeManager(trade)
        return await manager.update_trade(trade_id)
    except Exception as e:
        raise e

@router.delete("/delete_trade/{trade_id}", tags=["Trades"])
async def delete_trade(trade_id: UUID):
    try:
        manager = TradeManager(None)
        return await manager.delete_trade(trade_id)
    except Exception as e:
        raise e

@router.delete("/delete_trades", tags=["Trades"])
async def delete_trades():
    try:
        manager = TradeManager(None)
        return await manager.delete_trades()
    except Exception as e:
        raise e

# Trade Cost Routers

@router.get("/trade_costs", tags=["Trade Costs"])
async def get_trade_costs():
    try:
        manager = TradeCostManager(None)
        return await manager.get_trade_costs()
    except Exception as e:
        raise e

@router.get("/trade_costs/{trade_cost_id}", tags=["Trade Costs"])
async def get_trade_cost(trade_cost_id: UUID):
    try:
        manager = TradeCostManager(None)
        return await manager.get_trade_cost(trade_cost_id)
    except Exception as e:
        raise e

@router.post("/add_trade_cost", tags=["Trade Costs"])
async def add_trade_cost(trade_cost: TradeCostBase):
    try:
        manager = TradeCostManager(trade_cost)
        return await manager.add_trade_cost()
    except Exception as e:
        raise e

@router.put("/update_trade_cost/{trade_cost_id}", tags=["Trade Costs"])
async def update_trade_cost(trade_cost_id: UUID, trade_cost: TradeCostBase):
    try:
        manager = TradeCostManager(trade_cost)
        return await manager.update_trade_cost(trade_cost_id)
    except Exception as e:
        raise e

@router.delete("/delete_trade_cost/{trade_cost_id}", tags=["Trade Costs"])
async def delete_trade_cost(trade_cost_id: UUID):
    try:
        manager = TradeCostManager(None)
        return await manager.delete_trade_cost(trade_cost_id)
    except Exception as e:
        raise e

@router.delete("/delete_trade_costs", tags=["Trade Costs"])
async def delete_trade_costs():
    try:
        manager = TradeCostManager(None)
        return await manager.delete_trade_costs()
    except Exception as e:
        raise e

# Brokerage Deal Routers

@router.get("/brokerage_deals", tags=["Brokerage Deals"])
async def get_brokerage_deals():
    try:
        manager = BrokerageDealManager(None)
        return await manager.get_brokerage_deals()
    except Exception as e:
        raise e

@router.get("/brokerage_deals/{brokerage_deal_id}", tags=["Brokerage Deals"])
async def get_brokerage_deal(brokerage_deal_id: UUID):
    try:
        manager = BrokerageDealManager(None)
        return await manager.get_brokerage_deal(brokerage_deal_id)
    except Exception as e:
        raise e

@router.post("/add_brokerage_deal", tags=["Brokerage Deals"])
async def add_brokerage_deal(brokerage_deal: BrokerageDealBase):
    try:
        manager = BrokerageDealManager(brokerage_deal)
        return await manager.add_brokerage_deal()
    except Exception as e:
        raise e

@router.put("/update_brokerage_deal/{brokerage_deal_id}", tags=["Brokerage Deals"])
async def update_brokerage_deal(brokerage_deal_id: UUID, brokerage_deal: BrokerageDealBase):
    try:
        manager = BrokerageDealManager(brokerage_deal)
        return await manager.update_brokerage_deal(brokerage_deal_id)
    except Exception as e:
        raise e

@router.delete("/delete_brokerage_deal/{brokerage_deal_id}", tags=["Brokerage Deals"])
async def delete_brokerage_deal(brokerage_deal_id: UUID):
    try:
        manager = BrokerageDealManager(None)
        return await manager.delete_brokerage_deal(brokerage_deal_id)
    except Exception as e:
        raise e

@router.delete("/delete_brokerage_deals", tags=["Brokerage Deals"])
async def delete_brokerage_deals():
    try:
        manager = BrokerageDealManager(None)
        return await manager.delete_brokerage_deals()
    except Exception as e:
        raise e

# Shipment Routers

@router.get("/shipments", tags=["Shipments"])
async def get_shipments():
    try:
        manager = ShipmentManager(None)
        return await manager.get_shipments()
    except Exception as e:
        raise e

@router.get("/shipments/{shipment_id}", tags=["Shipments"])
async def get_shipment(shipment_id: UUID):
    try:
        manager = ShipmentManager(None)
        return await manager.get_shipment(shipment_id)
    except Exception as e:
        raise e

@router.post("/add_shipment", tags=["Shipments"])
async def add_shipment(shipment: ShipmentBase):
    try:
        manager = ShipmentManager(shipment)
        return await manager.add_shipment()
    except Exception as e:
        raise e

@router.put("/update_shipment/{shipment_id}", tags=["Shipments"])
async def update_shipment(shipment_id: UUID, shipment: ShipmentBase):
    try:
        manager = ShipmentManager(shipment)
        return await manager.update_shipment(shipment_id)
    except Exception as e:
        raise e

@router.delete("/delete_shipment/{shipment_id}", tags=["Shipments"])
async def delete_shipment(shipment_id: UUID):
    try:
        manager = ShipmentManager(None)
        return await manager.delete_shipment(shipment_id)
    except Exception as e:
        raise e

@router.delete("/delete_shipments", tags=["Shipments"])
async def delete_shipments():
    try:
        manager = ShipmentManager(None)
        return await manager.delete_shipments()
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

# Share Transaction Routers

@router.get("/share_transactions", tags=["Share Transactions"])
async def get_share_transactions():
    try:
        manager = ShareTransactionManager(None)
        return await manager.get_share_transactions()
    except Exception as e:
        raise e

@router.get("/share_transactions/{share_transaction_id}", tags=["Share Transactions"])
async def get_share_transaction(share_transaction_id: UUID):
    try:
        manager = ShareTransactionManager(None)
        return await manager.get_share_transaction(share_transaction_id)
    except Exception as e:
        raise e

@router.post("/add_share_transaction", tags=["Share Transactions"])
async def add_share_transaction(share_transaction: ShareTransactionBase):
    try:
        manager = ShareTransactionManager(share_transaction)
        return await manager.add_share_transaction()
    except Exception as e:
        raise e

@router.put("/update_share_transaction/{share_transaction_id}", tags=["Share Transactions"])
async def update_share_transaction(share_transaction_id: UUID, share_transaction: ShareTransactionBase):
    try:
        manager = ShareTransactionManager(share_transaction)
        return await manager.update_share_transaction(share_transaction_id)
    except Exception as e:
        raise e

@router.delete("/delete_share_transaction/{share_transaction_id}", tags=["Share Transactions"])
async def delete_share_transaction(share_transaction_id: UUID):
    try:
        manager = ShareTransactionManager(None)
        return await manager.delete_share_transaction(share_transaction_id)
    except Exception as e:
        raise e

@router.delete("/delete_share_transactions", tags=["Share Transactions"])
async def delete_share_transactions():
    try:
        manager = ShareTransactionManager(None)
        return await manager.delete_share_transactions()
    except Exception as e:
        raise e