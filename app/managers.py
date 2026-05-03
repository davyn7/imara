# app/managers.py

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
from app.db import (
    get_companies_db,
    get_company_db,
    add_company_db,
    update_company_db,
    delete_company_db,
    delete_companies_db,
    get_counterparties_db,
    get_counterparty_db,
    add_counterparty_db,
    update_counterparty_db,
    delete_counterparty_db,
    delete_counterparties_db,
    get_shareholders_db,
    get_shareholder_db,
    add_shareholder_db,
    update_shareholder_db,
    delete_shareholder_db,
    delete_shareholders_db,
    get_equity_rounds_db,
    get_equity_round_db,
    add_equity_round_db,
    update_equity_round_db,
    delete_equity_round_db,
    delete_equity_rounds_db
)
from uuid import UUID

# Activity Log Manager
# TODO: Implement Activity Log Manager
class ActivityLogManager:
    def __init__(self, activity_log: ActivityLogBase):
        self.activity_log = activity_log

# Company Manager

class CompanyManager:
    def __init__(self, company: CompanyBase):
        self.company = company

    async def get_companies(self):
        return await get_companies_db()

    async def get_company(self, company_id: UUID):
        return await get_company_db(company_id)

    async def add_company(self):
        return await add_company_db(self.company)
    
    async def update_company(self, company_id: UUID):
        return await update_company_db(self.company, company_id)
    
    async def delete_company(self, company_id: UUID):
        return await delete_company_db(company_id)

    async def delete_companies(self):
        return await delete_companies_db()

# Counterparty Manager
# TODO: Implement Counterparty Manager
class CounterpartyManager:
    def __init__(self, counterparty: CounterpartyBase):
        self.counterparty = counterparty
    
    async def get_counterparties(self):
        return await get_counterparties_db()

    async def get_counterparty(self, counterparty_id: UUID):
        return await get_counterparty_db(counterparty_id)

    async def add_counterparty(self):
        return await add_counterparty_db(self.counterparty)
    
    async def update_counterparty(self, counterparty_id: UUID):
        return await update_counterparty_db(self.counterparty, counterparty_id)
    
    async def delete_counterparty(self, counterparty_id: UUID):
        return await delete_counterparty_db(counterparty_id)
    
    async def delete_counterparties(self):
        return await delete_counterparties_db()

# Trade Manager
# TODO: Implement Trade Manager
class TradeManager:
    def __init__(self, trade: TradeBase):
        self.trade = trade

# Trade Cost Manager
# TODO: Implement Trade Cost Manager
class TradeCostManager:
    def __init__(self, trade_cost: TradeCostBase):
        self.trade_cost = trade_cost

# Brokerage Deal Manager
# TODO: Implement Brokerage Deal Manager
class BrokerageDealManager:
    def __init__(self, brokerage_deal: BrokerageDealBase):
        self.brokerage_deal = brokerage_deal

# Shipment Manager
# TODO: Implement Shipment Manager
class ShipmentManager:
    def __init__(self, shipment: ShipmentBase):
        self.shipment = shipment

# Shareholder Manager

class ShareholderManager:
    def __init__(self, shareholder: ShareholderBase):
        self.shareholder = shareholder
    
    async def get_shareholders(self):
        return await get_shareholders_db()

    async def get_shareholder(self, shareholder_id: UUID):
        return await get_shareholder_db(shareholder_id)

    async def add_shareholder(self):
        return await add_shareholder_db(self.shareholder)
    
    async def update_shareholder(self, shareholder_id: UUID):
        return await update_shareholder_db(self.shareholder, shareholder_id)
    
    async def delete_shareholder(self, shareholder_id: UUID):
        return await delete_shareholder_db(shareholder_id)

    async def delete_shareholders(self):
        return await delete_shareholders_db()

# Equity Round Manager

class EquityRoundManager:
    def __init__(self, equity_round: EquityRoundBase):
        self.equity_round = equity_round

    async def get_equity_rounds(self):
        return await get_equity_rounds_db()

    async def get_equity_round(self, equity_round_id: UUID):
        return await get_equity_round_db(equity_round_id)

    async def add_equity_round(self):
        return await add_equity_round_db(self.equity_round)

    async def update_equity_round(self, equity_round_id: UUID):
        return await update_equity_round_db(self.equity_round, equity_round_id)

    async def delete_equity_round(self, equity_round_id: UUID):
        return await delete_equity_round_db(equity_round_id)

    async def delete_equity_rounds(self):
        return await delete_equity_rounds_db()
        
# Share Transaction Manager
# TODO: Implement Share Transaction Manager
class ShareTransactionManager:
    def __init__(self, share_transaction: ShareTransactionBase):
        self.share_transaction = share_transaction

    def shares_calculation(self):
        if self.equity_round.pre_money_valuation:
            self.equity_round.post_money_valuation = self.equity_round.pre_money_valuation + self.equity_round.total_raised
        if self.equity_round.post_money_valuation:
            self.equity_round.pre_money_valuation = self.equity_round.post_money_valuation - self.equity_round.total_raised
        pass
