from app.connection import supabase
from app.schemas import (
    ActivityLogBase,
    CompanyBase,
    BankAccountBase,
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

# Company DB Operations

async def get_companies_db():
    response = supabase.table("companies").select("*").execute()
    return response.data

async def get_company_db(company_id: UUID):
    response = supabase.table("companies").select("*").eq("id", company_id).execute()
    return response.data

async def add_company_db(company: CompanyBase):
    company_data = company.model_dump()
    response = supabase.table("companies").insert(company_data).execute()
    return response.data

async def update_company_db(company: CompanyBase, company_id: UUID):
    company_data = company.model_dump(exclude_unset=True)
    response = supabase.table("companies").update(company_data).eq("id", company_id).execute()
    return response.data

async def delete_company_db(company_id: UUID):
    response = supabase.table("companies").delete().eq("id", company_id).execute()
    return response.data

async def delete_companies_db():
    response = supabase.table("companies").delete().neq("id", "00000000-0000-0000-0000-000000000000").execute()
    return response.data   

# Bank Account DB Operations

async def get_bank_accounts_db():
    response = supabase.table("bank_accounts").select("*").execute()
    return response.data

async def get_bank_account_db(bank_account_id: UUID):
    response = supabase.table("bank_accounts").select("*").eq("id", bank_account_id).execute()
    return response.data

async def add_bank_account_db(bank_account: BankAccountBase):
    bank_account_data = bank_account.model_dump(mode="json")
    response = supabase.table("bank_accounts").insert(bank_account_data).execute()
    return response.data

async def update_bank_account_db(bank_account: BankAccountBase, bank_account_id: UUID):
    bank_account_data = bank_account.model_dump(mode="json", exclude_unset=True)
    response = supabase.table("bank_accounts").update(bank_account_data).eq("id", bank_account_id).execute()
    return response.data

async def delete_bank_account_db(bank_account_id: UUID):
    response = supabase.table("bank_accounts").delete().eq("id", bank_account_id).execute()
    return response.data

async def delete_bank_accounts_db():
    response = supabase.table("bank_accounts").delete().neq("id", "00000000-0000-0000-0000-000000000000").execute()
    return response.data

# Counterparty DB Operations

async def get_counterparties_db():
    response = supabase.table("counterparties").select("*").execute()
    return response.data

async def get_counterparty_db(counterparty_id: UUID):
    response = supabase.table("counterparties").select("*").eq("id", counterparty_id).execute()
    return response.data

async def add_counterparty_db(counterparty: CounterpartyBase):
    counterparty_data = counterparty.model_dump(mode="json")
    response = supabase.table("counterparties").insert(counterparty_data).execute()
    return response.data

async def update_counterparty_db(counterparty: CounterpartyBase, counterparty_id: UUID):
    counterparty_data = counterparty.model_dump(mode="json", exclude_unset=True)
    response = supabase.table("counterparties").update(counterparty_data).eq("id", counterparty_id).execute()
    return response.data

async def delete_counterparty_db(counterparty_id: UUID):
    response = supabase.table("counterparties").delete().eq("id", counterparty_id).execute()
    return response.data

async def delete_counterparties_db():
    response = supabase.table("counterparties").delete().neq("id", "00000000-0000-0000-0000-000000000000").execute()
    return response.data

# Trade DB Operations

async def get_trades_db():
    response = supabase.table("trades").select("*").execute()
    return response.data

async def get_trade_db(trade_id: UUID):
    response = supabase.table("trades").select("*").eq("id", trade_id).execute()
    return response.data

async def add_trade_db(trade: TradeBase):
    trade_data = trade.model_dump(mode="json")
    response = supabase.table("trades").insert(trade_data).execute()
    return response.data

async def update_trade_db(trade: TradeBase, trade_id: UUID):
    trade_data = trade.model_dump(mode="json", exclude_unset=True)
    response = supabase.table("trades").update(trade_data).eq("id", trade_id).execute()
    return response.data

async def delete_trade_db(trade_id: UUID):
    response = supabase.table("trades").delete().eq("id", trade_id).execute()
    return response.data

async def delete_trades_db():
    response = supabase.table("trades").delete().neq("id", "00000000-0000-0000-0000-000000000000").execute()
    return response.data

# Trade Cost DB Operations

async def get_trade_costs_db():
    response = supabase.table("trade_costs").select("*").execute()
    return response.data

async def get_trade_cost_db(trade_cost_id: UUID):
    response = supabase.table("trade_costs").select("*").eq("id", trade_cost_id).execute()
    return response.data

async def add_trade_cost_db(trade_cost: TradeCostBase):
    trade_cost_data = trade_cost.model_dump(mode="json")
    response = supabase.table("trade_costs").insert(trade_cost_data).execute()
    return response.data

async def update_trade_cost_db(trade_cost: TradeCostBase, trade_cost_id: UUID):
    trade_cost_data = trade_cost.model_dump(mode="json", exclude_unset=True)
    response = supabase.table("trade_costs").update(trade_cost_data).eq("id", trade_cost_id).execute()
    return response.data

async def delete_trade_cost_db(trade_cost_id: UUID):
    response = supabase.table("trade_costs").delete().eq("id", trade_cost_id).execute()
    return response.data

async def delete_trade_costs_db():
    response = supabase.table("trade_costs").delete().neq("id", "00000000-0000-0000-0000-000000000000").execute()
    return response.data

# Brokerage Deal DB Operations

async def get_brokerage_deals_db():
    response = supabase.table("brokerage_deals").select("*").execute()
    return response.data

async def get_brokerage_deal_db(brokerage_deal_id: UUID):
    response = supabase.table("brokerage_deals").select("*").eq("id", brokerage_deal_id).execute()
    return response.data

async def add_brokerage_deal_db(brokerage_deal: BrokerageDealBase):
    brokerage_deal_data = brokerage_deal.model_dump(mode="json")
    response = supabase.table("brokerage_deals").insert(brokerage_deal_data).execute()
    return response.data

async def update_brokerage_deal_db(brokerage_deal: BrokerageDealBase, brokerage_deal_id: UUID):
    brokerage_deal_data = brokerage_deal.model_dump(mode="json", exclude_unset=True)
    response = supabase.table("brokerage_deals").update(brokerage_deal_data).eq("id", brokerage_deal_id).execute()
    return response.data

async def delete_brokerage_deal_db(brokerage_deal_id: UUID):
    response = supabase.table("brokerage_deals").delete().eq("id", brokerage_deal_id).execute()
    return response.data

async def delete_brokerage_deals_db():
    response = supabase.table("brokerage_deals").delete().neq("id", "00000000-0000-0000-0000-000000000000").execute()
    return response.data

# Shipment DB Operations

async def get_shipments_db():
    response = supabase.table("shipments").select("*").execute()
    return response.data

async def get_shipment_db(shipment_id: UUID):
    response = supabase.table("shipments").select("*").eq("id", shipment_id).execute()
    return response.data

async def add_shipment_db(shipment: ShipmentBase):
    shipment_data = shipment.model_dump(mode="json")
    response = supabase.table("shipments").insert(shipment_data).execute()
    return response.data

async def update_shipment_db(shipment: ShipmentBase, shipment_id: UUID):
    shipment_data = shipment.model_dump(mode="json", exclude_unset=True)
    response = supabase.table("shipments").update(shipment_data).eq("id", shipment_id).execute()
    return response.data

async def delete_shipment_db(shipment_id: UUID):
    response = supabase.table("shipments").delete().eq("id", shipment_id).execute()
    return response.data

async def delete_shipments_db():
    response = supabase.table("shipments").delete().neq("id", "00000000-0000-0000-0000-000000000000").execute()
    return response.data

# Shareholder DB Operations

async def get_shareholders_db():
    response = supabase.table("shareholders").select("*").execute()
    return response.data

async def get_shareholder_db(shareholder_id: UUID):
    response = supabase.table("shareholders").select("*").eq("id", shareholder_id).execute()
    return response.data

async def add_shareholder_db(shareholder: ShareholderBase):
    shareholder_data = shareholder.model_dump(mode="json")
    response = supabase.table("shareholders").insert(shareholder_data).execute()
    return response.data

async def update_shareholder_db(shareholder: ShareholderBase, shareholder_id: UUID):
    shareholder_data = shareholder.model_dump(mode="json", exclude_unset=True)
    response = supabase.table("shareholders").update(shareholder_data).eq("id", shareholder_id).execute()
    return response.data

async def delete_shareholder_db(shareholder_id: UUID):
    response = supabase.table("shareholders").delete().eq("id", shareholder_id).execute()
    return response.data

async def delete_shareholders_db():
    response = supabase.table("shareholders").delete().neq("id", "00000000-0000-0000-0000-000000000000").execute()
    return response.data

# Equity Round DB Operations

async def get_equity_rounds_db():
    response = supabase.table("equity_rounds").select("*").execute()
    return response.data

async def get_equity_round_db(equity_round_id: UUID):
    response = supabase.table("equity_rounds").select("*").eq("id", equity_round_id).execute()
    return response.data

async def add_equity_round_db(equity_round: EquityRoundBase):
    equity_round_data = equity_round.model_dump(mode="json")
    response = supabase.table("equity_rounds").insert(equity_round_data).execute()
    return response.data

async def update_equity_round_db(equity_round: EquityRoundBase, equity_round_id: UUID):
    equity_round_data = equity_round.model_dump(mode="json", exclude_unset=True)
    response = supabase.table("equity_rounds").update(equity_round_data).eq("id", equity_round_id).execute()
    return response.data

async def delete_equity_round_db(equity_round_id: UUID):
    response = supabase.table("equity_rounds").delete().eq("id", equity_round_id).execute()
    return response.data

async def delete_equity_rounds_db():
    response = supabase.table("equity_rounds").delete().neq("id", "00000000-0000-0000-0000-000000000000").execute()
    return response.data

# Share Transaction DB Operations

async def get_share_transactions_db():
    response = supabase.table("share_transactions").select("*").execute()
    return response.data

async def get_share_transaction_db(share_transaction_id: UUID):
    response = supabase.table("share_transactions").select("*").eq("id", share_transaction_id).execute()
    return response.data

async def add_share_transaction_db(share_transaction: ShareTransactionBase):
    share_transaction_data = share_transaction.model_dump(mode="json")
    response = supabase.table("share_transactions").insert(share_transaction_data).execute()
    return response.data

async def update_share_transaction_db(share_transaction: ShareTransactionBase, share_transaction_id: UUID):
    share_transaction_data = share_transaction.model_dump(mode="json", exclude_unset=True)
    response = supabase.table("share_transactions").update(share_transaction_data).eq("id", share_transaction_id).execute()
    return response.data

async def delete_share_transaction_db(share_transaction_id: UUID):
    response = supabase.table("share_transactions").delete().eq("id", share_transaction_id).execute()
    return response.data

async def delete_share_transactions_db():
    response = supabase.table("share_transactions").delete().neq("id", "00000000-0000-0000-0000-000000000000").execute()
    return response.data