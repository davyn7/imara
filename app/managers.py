# app/managers.py

from app.schemas import (
    ActivityLogBase,
    CompanyBase,
    BankAccountBase,
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
    get_bank_accounts_db,
    get_bank_account_db,
    add_bank_account_db,
    update_bank_account_db,
    delete_bank_account_db,
    delete_bank_accounts_db,
    get_trades_db,
    get_trade_db,
    add_trade_db,
    update_trade_db,
    delete_trade_db,
    delete_trades_db,
    get_trade_costs_db,
    get_trade_cost_db,
    add_trade_cost_db,
    update_trade_cost_db,
    delete_trade_cost_db,
    delete_trade_costs_db,
    get_brokerage_deals_db,
    get_brokerage_deal_db,
    add_brokerage_deal_db,
    update_brokerage_deal_db,
    delete_brokerage_deal_db,
    delete_brokerage_deals_db,
    get_shipments_db,
    get_shipment_db,
    add_shipment_db,
    update_shipment_db,
    delete_shipment_db,
    delete_shipments_db,
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
    delete_equity_rounds_db,
    get_share_transactions_db,
    get_share_transaction_db,
    add_share_transaction_db,
    update_share_transaction_db,
    delete_share_transaction_db,
    delete_share_transactions_db
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

# Bank Account Manager

class BankAccountManager:
    def __init__(self, bank_account: BankAccountBase):
        self.bank_account = bank_account
    
    async def get_bank_accounts(self):
        return await get_bank_accounts_db()

    async def get_bank_account(self, bank_account_id: UUID):
        return await get_bank_account_db(bank_account_id)

    async def add_bank_account(self):
        return await add_bank_account_db(self.bank_account)
    
    async def update_bank_account(self, bank_account_id: UUID):
        return await update_bank_account_db(self.bank_account, bank_account_id)
    
    async def delete_bank_account(self, bank_account_id: UUID):
        return await delete_bank_account_db(bank_account_id)
    
    async def delete_bank_accounts(self):
        return await delete_bank_accounts_db()

# Trade Manager
# TODO: Implement Trade Manager
class TradeManager:
    def __init__(self, trade: TradeBase):
        self.trade = trade
    
    async def get_trades(self):
        return await get_trades_db()

    async def get_trade(self, trade_id: UUID):
        return await get_trade_db(trade_id)

    async def add_trade(self):
        return await add_trade_db(self.trade)
    
    async def update_trade(self, trade_id: UUID):
        return await update_trade_db(self.trade, trade_id)
    
    async def delete_trade(self, trade_id: UUID):
        return await delete_trade_db(trade_id)

    async def delete_trades(self):
        return await delete_trades_db()

# Trade Cost Manager
# TODO: Implement Trade Cost Manager
class TradeCostManager:
    def __init__(self, trade_cost: TradeCostBase):
        self.trade_cost = trade_cost

    async def get_trade_costs(self):
        return await get_trade_costs_db()

    async def get_trade_cost(self, trade_cost_id: UUID):
        return await get_trade_cost_db(trade_cost_id)

    async def add_trade_cost(self):
        return await add_trade_cost_db(self.trade_cost)
    
    async def update_trade_cost(self, trade_cost_id: UUID):
        return await update_trade_cost_db(self.trade_cost, trade_cost_id)
    
    async def delete_trade_cost(self, trade_cost_id: UUID):
        return await delete_trade_cost_db(trade_cost_id)
    
    async def delete_trade_costs(self):
        return await delete_trade_costs_db()

# Brokerage Deal Manager
# TODO: Implement Brokerage Deal Manager
class BrokerageDealManager:
    def __init__(self, brokerage_deal: BrokerageDealBase):
        self.brokerage_deal = brokerage_deal
    
    async def get_brokerage_deals(self):
        return await get_brokerage_deals_db()

    async def get_brokerage_deal(self, brokerage_deal_id: UUID):
        return await get_brokerage_deal_db(brokerage_deal_id)

    async def add_brokerage_deal(self):
        return await add_brokerage_deal_db(self.brokerage_deal)
    
    async def update_brokerage_deal(self, brokerage_deal_id: UUID):
        return await update_brokerage_deal_db(self.brokerage_deal, brokerage_deal_id)
    
    async def delete_brokerage_deal(self, brokerage_deal_id: UUID):
        return await delete_brokerage_deal_db(brokerage_deal_id)
    
    async def delete_brokerage_deals(self):
        return await delete_brokerage_deals_db()

# Shipment Manager
# TODO: Implement Shipment Manager
class ShipmentManager:
    def __init__(self, shipment: ShipmentBase):
        self.shipment = shipment

    async def get_shipments(self):
        return await get_shipments_db()

    async def get_shipment(self, shipment_id: UUID):
        return await get_shipment_db(shipment_id)

    async def add_shipment(self):
        return await add_shipment_db(self.shipment)
    
    async def update_shipment(self, shipment_id: UUID):
        return await update_shipment_db(self.shipment, shipment_id)
    
    async def delete_shipment(self, shipment_id: UUID):
        return await delete_shipment_db(shipment_id)
    
    async def delete_shipments(self):
        return await delete_shipments_db()

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

    async def get_share_transactions(self):
        return await get_share_transactions_db()

    async def get_share_transaction(self, share_transaction_id: UUID):
        return await get_share_transaction_db(share_transaction_id)

    async def add_share_transaction(self):
        return await add_share_transaction_db(self.share_transaction)
    
    async def update_share_transaction(self, share_transaction_id: UUID):
        return await update_share_transaction_db(self.share_transaction, share_transaction_id)
    
    async def delete_share_transaction(self, share_transaction_id: UUID):
        return await delete_share_transaction_db(share_transaction_id)

    async def delete_share_transactions(self):
        return await delete_share_transactions_db()
