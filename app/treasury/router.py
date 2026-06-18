# app/treasury/router.py

from fastapi import APIRouter, Query
from app.treasury.managers import (
    AccountManager,
    TreasuryTransactionManager,
    PayableManager,
    ReceivableManager,
    AccountTransferManager,
    ExpenseManager,
    ReimbursementManager,
    FxTransactionManager,
    BankStatementLineManager,
    ReconciliationManager,
    CashBalanceSnapshotManager,
    TreasurySummaryManager,
)
from app.treasury.schemas import (
    AccountBase,
    TreasuryTransactionBase,
    PayableBase,
    ReceivableBase,
    AccountTransferBase,
    ExpenseBase,
    ReimbursementBase,
    FxTransactionBase,
    BankStatementLineBase,
    ReconciliationBase,
    ReconciliationMatchBase,
    CashBalanceSnapshotBase,
)

router = APIRouter(prefix="/treasury", tags=["Treasury"])


# ============================================================
# Accounts
# ============================================================

@router.post("/accounts")
async def create_account(account: AccountBase):
    try:
        manager = AccountManager(account)
        return await manager.create_account()
    except Exception as e:
        raise e


@router.get("/accounts")
async def get_accounts():
    try:
        manager = AccountManager()
        return await manager.get_accounts()
    except Exception as e:
        raise e


@router.get("/companies/{company_id}/accounts")
async def get_accounts_by_company(company_id: int):
    try:
        manager = AccountManager()
        return await manager.get_accounts_by_company(company_id)
    except Exception as e:
        raise e


@router.get("/accounts/{account_id}/balance")
async def get_account_balance(account_id: int):
    try:
        manager = AccountManager()
        return await manager.get_account_balance(account_id)
    except Exception as e:
        raise e


@router.get("/accounts/{account_id}/expenses/by_month")
async def get_account_expenses_by_month(
    account_id: int,
    month: int = Query(..., ge=1, le=12),
    year: int = Query(..., ge=2000, le=2100),
):
    try:
        manager = AccountManager()
        return await manager.get_expenses_by_month_year(account_id, month, year)
    except Exception as e:
        raise e


@router.get("/accounts/{account_id}/expenses/total_by_month")
async def get_account_expense_total_by_month(
    account_id: int,
    month: int = Query(..., ge=1, le=12),
    year: int = Query(..., ge=2000, le=2100),
):
    try:
        manager = AccountManager()
        return await manager.get_expense_total_by_month_year(account_id, month, year)
    except Exception as e:
        raise e


@router.get("/accounts/{account_id}/expenses/monthly_totals")
async def get_account_monthly_expense_totals(account_id: int):
    try:
        manager = AccountManager()
        return await manager.get_monthly_expense_totals(account_id)
    except Exception as e:
        raise e


@router.get("/accounts/{account_id}/transactions")
async def get_transactions_by_account(account_id: int):
    try:
        manager = TreasuryTransactionManager()
        return await manager.get_transactions_by_account(account_id)
    except Exception as e:
        raise e


@router.get("/accounts/{account_id}/bank-statement-lines")
async def get_bank_statement_lines_by_account(account_id: int):
    try:
        manager = BankStatementLineManager()
        return await manager.get_bank_statement_lines_by_account(account_id)
    except Exception as e:
        raise e


@router.get("/accounts/{account_id}/cash-balance-snapshots")
async def get_cash_balance_snapshots_by_account(account_id: int):
    try:
        manager = CashBalanceSnapshotManager()
        return await manager.get_cash_balance_snapshots_by_account(account_id)
    except Exception as e:
        raise e


@router.get("/accounts/{account_id}")
async def get_account_by_id(account_id: int):
    try:
        manager = AccountManager()
        return await manager.get_account(account_id)
    except Exception as e:
        raise e


@router.patch("/accounts/{account_id}")
async def update_account(account_id: int, account: AccountBase):
    try:
        manager = AccountManager(account)
        return await manager.update_account(account_id)
    except Exception as e:
        raise e


@router.delete("/accounts/{account_id}")
async def delete_account(account_id: int):
    try:
        manager = AccountManager()
        return await manager.delete_account(account_id)
    except Exception as e:
        raise e


# ============================================================
# Treasury Transactions
# ============================================================

@router.post("/transactions")
async def create_transaction(transaction: TreasuryTransactionBase):
    try:
        manager = TreasuryTransactionManager(transaction)
        return await manager.create_transaction()
    except Exception as e:
        raise e


@router.get("/transactions")
async def get_transactions():
    try:
        manager = TreasuryTransactionManager()
        return await manager.get_transactions()
    except Exception as e:
        raise e


@router.get("/trades/{trade_id}/transactions")
async def get_transactions_by_trade(trade_id: int):
    try:
        manager = TreasuryTransactionManager()
        return await manager.get_transactions_by_trade(trade_id)
    except Exception as e:
        raise e


@router.get("/shipments/{shipment_id}/transactions")
async def get_transactions_by_shipment(shipment_id: int):
    try:
        manager = TreasuryTransactionManager()
        return await manager.get_transactions_by_shipment(shipment_id)
    except Exception as e:
        raise e


@router.get("/transactions/{transaction_id}")
async def get_transaction_by_id(transaction_id: int):
    try:
        manager = TreasuryTransactionManager()
        return await manager.get_transaction(transaction_id)
    except Exception as e:
        raise e


@router.patch("/transactions/{transaction_id}")
async def update_transaction(transaction_id: int, transaction: TreasuryTransactionBase):
    try:
        manager = TreasuryTransactionManager(transaction)
        return await manager.update_transaction(transaction_id)
    except Exception as e:
        raise e


@router.delete("/transactions/{transaction_id}")
async def delete_transaction(transaction_id: int):
    try:
        manager = TreasuryTransactionManager()
        return await manager.delete_transaction(transaction_id)
    except Exception as e:
        raise e


@router.post("/transactions/{transaction_id}/complete")
async def complete_transaction(transaction_id: int):
    try:
        manager = TreasuryTransactionManager()
        return await manager.complete_transaction(transaction_id)
    except Exception as e:
        raise e


@router.post("/transactions/{transaction_id}/cancel")
async def cancel_transaction(transaction_id: int):
    try:
        manager = TreasuryTransactionManager()
        return await manager.cancel_transaction(transaction_id)
    except Exception as e:
        raise e


@router.post("/transactions/{transaction_id}/reconcile")
async def reconcile_transaction(transaction_id: int):
    try:
        manager = TreasuryTransactionManager()
        return await manager.reconcile_transaction(transaction_id)
    except Exception as e:
        raise e


# ============================================================
# Payables
# ============================================================

@router.post("/payables")
async def create_payable(payable: PayableBase):
    try:
        manager = PayableManager(payable)
        return await manager.create_payable()
    except Exception as e:
        raise e


@router.get("/payables")
async def get_payables():
    try:
        manager = PayableManager()
        return await manager.get_payables()
    except Exception as e:
        raise e


@router.get("/trades/{trade_id}/payables")
async def get_payables_by_trade(trade_id: int):
    try:
        manager = PayableManager()
        return await manager.get_payables_by_trade(trade_id)
    except Exception as e:
        raise e


@router.get("/counterparties/{counterparty_id}/payables")
async def get_payables_by_counterparty(counterparty_id: int):
    try:
        manager = PayableManager()
        return await manager.get_payables_by_counterparty(counterparty_id)
    except Exception as e:
        raise e


@router.get("/payables/{payable_id}")
async def get_payable_by_id(payable_id: int):
    try:
        manager = PayableManager()
        return await manager.get_payable(payable_id)
    except Exception as e:
        raise e


@router.patch("/payables/{payable_id}")
async def update_payable(payable_id: int, payable: PayableBase):
    try:
        manager = PayableManager(payable)
        return await manager.update_payable(payable_id)
    except Exception as e:
        raise e


@router.delete("/payables/{payable_id}")
async def delete_payable(payable_id: int):
    try:
        manager = PayableManager()
        return await manager.delete_payable(payable_id)
    except Exception as e:
        raise e


@router.post("/payables/{payable_id}/approve")
async def approve_payable(payable_id: int):
    try:
        manager = PayableManager()
        return await manager.approve_payable(payable_id)
    except Exception as e:
        raise e


@router.post("/payables/{payable_id}/schedule")
async def schedule_payable(payable_id: int):
    try:
        manager = PayableManager()
        return await manager.schedule_payable(payable_id)
    except Exception as e:
        raise e


@router.post("/payables/{payable_id}/mark-paid")
async def mark_payable_as_paid(payable_id: int):
    try:
        manager = PayableManager()
        return await manager.mark_payable_as_paid(payable_id)
    except Exception as e:
        raise e


@router.post("/payables/{payable_id}/cancel")
async def cancel_payable(payable_id: int):
    try:
        manager = PayableManager()
        return await manager.cancel_payable(payable_id)
    except Exception as e:
        raise e


# ============================================================
# Receivables
# ============================================================

@router.post("/receivables")
async def create_receivable(receivable: ReceivableBase):
    try:
        manager = ReceivableManager(receivable)
        return await manager.create_receivable()
    except Exception as e:
        raise e


@router.get("/receivables")
async def get_receivables():
    try:
        manager = ReceivableManager()
        return await manager.get_receivables()
    except Exception as e:
        raise e


@router.get("/trades/{trade_id}/receivables")
async def get_receivables_by_trade(trade_id: int):
    try:
        manager = ReceivableManager()
        return await manager.get_receivables_by_trade(trade_id)
    except Exception as e:
        raise e


@router.get("/counterparties/{counterparty_id}/receivables")
async def get_receivables_by_counterparty(counterparty_id: int):
    try:
        manager = ReceivableManager()
        return await manager.get_receivables_by_counterparty(counterparty_id)
    except Exception as e:
        raise e


@router.get("/receivables/{receivable_id}")
async def get_receivable_by_id(receivable_id: int):
    try:
        manager = ReceivableManager()
        return await manager.get_receivable(receivable_id)
    except Exception as e:
        raise e


@router.patch("/receivables/{receivable_id}")
async def update_receivable(receivable_id: int, receivable: ReceivableBase):
    try:
        manager = ReceivableManager(receivable)
        return await manager.update_receivable(receivable_id)
    except Exception as e:
        raise e


@router.delete("/receivables/{receivable_id}")
async def delete_receivable(receivable_id: int):
    try:
        manager = ReceivableManager()
        return await manager.delete_receivable(receivable_id)
    except Exception as e:
        raise e


@router.post("/receivables/{receivable_id}/invoice")
async def mark_receivable_as_invoiced(receivable_id: int):
    try:
        manager = ReceivableManager()
        return await manager.mark_receivable_as_invoiced(receivable_id)
    except Exception as e:
        raise e


@router.post("/receivables/{receivable_id}/mark-received")
async def mark_receivable_as_received(receivable_id: int):
    try:
        manager = ReceivableManager()
        return await manager.mark_receivable_as_received(receivable_id)
    except Exception as e:
        raise e


@router.post("/receivables/{receivable_id}/cancel")
async def cancel_receivable(receivable_id: int):
    try:
        manager = ReceivableManager()
        return await manager.cancel_receivable(receivable_id)
    except Exception as e:
        raise e


# ============================================================
# Account Transfers
# ============================================================

@router.post("/transfers")
async def create_account_transfer(transfer: AccountTransferBase):
    try:
        manager = AccountTransferManager(transfer)
        return await manager.create_transfer()
    except Exception as e:
        raise e


@router.get("/transfers")
async def get_account_transfers():
    try:
        manager = AccountTransferManager()
        return await manager.get_transfers()
    except Exception as e:
        raise e


@router.get("/transfers/{transfer_id}")
async def get_account_transfer_by_id(transfer_id: int):
    try:
        manager = AccountTransferManager()
        return await manager.get_transfer(transfer_id)
    except Exception as e:
        raise e


@router.patch("/transfers/{transfer_id}")
async def update_account_transfer(transfer_id: int, transfer: AccountTransferBase):
    try:
        manager = AccountTransferManager(transfer)
        return await manager.update_transfer(transfer_id)
    except Exception as e:
        raise e


@router.delete("/transfers/{transfer_id}")
async def delete_account_transfer(transfer_id: int):
    try:
        manager = AccountTransferManager()
        return await manager.delete_transfer(transfer_id)
    except Exception as e:
        raise e


@router.post("/transfers/{transfer_id}/complete")
async def complete_account_transfer(transfer_id: int):
    try:
        manager = AccountTransferManager()
        return await manager.complete_transfer(transfer_id)
    except Exception as e:
        raise e


@router.post("/transfers/{transfer_id}/cancel")
async def cancel_account_transfer(transfer_id: int):
    try:
        manager = AccountTransferManager()
        return await manager.cancel_transfer(transfer_id)
    except Exception as e:
        raise e


# ============================================================
# Expenses
# ============================================================

@router.post("/expenses")
async def create_expense(expense: ExpenseBase):
    try:
        manager = ExpenseManager(expense)
        return await manager.create_expense()
    except Exception as e:
        raise e


@router.get("/expenses")
async def get_expenses():
    try:
        manager = ExpenseManager()
        return await manager.get_expenses()
    except Exception as e:
        raise e


@router.get("/expenses/by_month")
async def get_expenses_by_month(
    month: int = Query(..., ge=1, le=12),
    year: int = Query(..., ge=2000, le=2100),
):
    try:
        manager = ExpenseManager()
        return await manager.get_expenses_by_month_year(month, year)
    except Exception as e:
        raise e


@router.get("/expenses/total_by_month")
async def get_expense_total_by_month(
    month: int = Query(..., ge=1, le=12),
    year: int = Query(..., ge=2000, le=2100),
):
    try:
        manager = ExpenseManager()
        return await manager.get_expense_total_by_month_year(month, year)
    except Exception as e:
        raise e


@router.get("/expenses/monthly_totals")
async def get_monthly_expense_totals():
    try:
        manager = ExpenseManager()
        return await manager.get_monthly_expense_totals()
    except Exception as e:
        raise e


@router.get("/companies/{company_id}/expenses")
async def get_expenses_by_company(company_id: int):
    try:
        manager = ExpenseManager()
        return await manager.get_expenses_by_company(company_id)
    except Exception as e:
        raise e


@router.get("/trades/{trade_id}/expenses")
async def get_expenses_by_trade(trade_id: int):
    try:
        manager = ExpenseManager()
        return await manager.get_expenses_by_trade(trade_id)
    except Exception as e:
        raise e


@router.get("/shipments/{shipment_id}/expenses")
async def get_expenses_by_shipment(shipment_id: int):
    try:
        manager = ExpenseManager()
        return await manager.get_expenses_by_shipment(shipment_id)
    except Exception as e:
        raise e


@router.get("/users/{user_id}/expenses/by_month")
async def get_user_expenses_by_month(
    user_id: int,
    month: int = Query(..., ge=1, le=12),
    year: int = Query(..., ge=2000, le=2100),
):
    try:
        manager = ExpenseManager()
        return await manager.get_expenses_by_user_month_year(user_id, month, year)
    except Exception as e:
        raise e


@router.get("/users/{user_id}/expenses/total_by_month")
async def get_user_expense_total_by_month(
    user_id: int,
    month: int = Query(..., ge=1, le=12),
    year: int = Query(..., ge=2000, le=2100),
):
    try:
        manager = ExpenseManager()
        return await manager.get_expense_total_by_user_month_year(user_id, month, year)
    except Exception as e:
        raise e


@router.get("/users/{user_id}/expenses/monthly_totals")
async def get_user_monthly_expense_totals(user_id: int):
    try:
        manager = ExpenseManager()
        return await manager.get_monthly_expense_totals_by_user(user_id)
    except Exception as e:
        raise e


@router.get("/expenses/{expense_id}")
async def get_expense_by_id(expense_id: int):
    try:
        manager = ExpenseManager()
        return await manager.get_expense(expense_id)
    except Exception as e:
        raise e


@router.patch("/expenses/{expense_id}")
async def update_expense(expense_id: int, expense: ExpenseBase):
    try:
        manager = ExpenseManager(expense)
        return await manager.update_expense(expense_id)
    except Exception as e:
        raise e


@router.delete("/expenses/{expense_id}")
async def delete_expense(expense_id: int):
    try:
        manager = ExpenseManager()
        return await manager.delete_expense(expense_id)
    except Exception as e:
        raise e


@router.post("/expenses/{expense_id}/submit")
async def submit_expense(expense_id: int):
    try:
        manager = ExpenseManager()
        return await manager.submit_expense(expense_id)
    except Exception as e:
        raise e


@router.post("/expenses/{expense_id}/approve")
async def approve_expense(expense_id: int):
    try:
        manager = ExpenseManager()
        return await manager.approve_expense(expense_id)
    except Exception as e:
        raise e


@router.post("/expenses/{expense_id}/reject")
async def reject_expense(expense_id: int):
    try:
        manager = ExpenseManager()
        return await manager.reject_expense(expense_id)
    except Exception as e:
        raise e


@router.post("/expenses/{expense_id}/mark-paid")
async def mark_expense_as_paid(expense_id: int):
    try:
        manager = ExpenseManager()
        return await manager.mark_expense_as_paid(expense_id)
    except Exception as e:
        raise e


# ============================================================
# Reimbursements
# ============================================================

@router.post("/reimbursements")
async def create_reimbursement(reimbursement: ReimbursementBase):
    try:
        manager = ReimbursementManager(reimbursement)
        return await manager.create_reimbursement()
    except Exception as e:
        raise e


@router.get("/reimbursements")
async def get_reimbursements():
    try:
        manager = ReimbursementManager()
        return await manager.get_reimbursements()
    except Exception as e:
        raise e


@router.get("/users/{user_id}/reimbursements")
async def get_reimbursements_by_user(user_id: int):
    try:
        manager = ReimbursementManager()
        return await manager.get_reimbursements_by_user(user_id)
    except Exception as e:
        raise e


@router.get("/reimbursements/{reimbursement_id}")
async def get_reimbursement_by_id(reimbursement_id: int):
    try:
        manager = ReimbursementManager()
        return await manager.get_reimbursement(reimbursement_id)
    except Exception as e:
        raise e


@router.patch("/reimbursements/{reimbursement_id}")
async def update_reimbursement(reimbursement_id: int, reimbursement: ReimbursementBase):
    try:
        manager = ReimbursementManager(reimbursement)
        return await manager.update_reimbursement(reimbursement_id)
    except Exception as e:
        raise e


@router.delete("/reimbursements/{reimbursement_id}")
async def delete_reimbursement(reimbursement_id: int):
    try:
        manager = ReimbursementManager()
        return await manager.delete_reimbursement(reimbursement_id)
    except Exception as e:
        raise e


@router.post("/reimbursements/{reimbursement_id}/approve")
async def approve_reimbursement(reimbursement_id: int):
    try:
        manager = ReimbursementManager()
        return await manager.approve_reimbursement(reimbursement_id)
    except Exception as e:
        raise e


@router.post("/reimbursements/{reimbursement_id}/reject")
async def reject_reimbursement(reimbursement_id: int):
    try:
        manager = ReimbursementManager()
        return await manager.reject_reimbursement(reimbursement_id)
    except Exception as e:
        raise e


@router.post("/reimbursements/{reimbursement_id}/mark-reimbursed")
async def mark_reimbursement_as_reimbursed(reimbursement_id: int):
    try:
        manager = ReimbursementManager()
        return await manager.mark_reimbursement_as_reimbursed(reimbursement_id)
    except Exception as e:
        raise e


# ============================================================
# FX Transactions
# ============================================================

@router.post("/fx-transactions")
async def create_fx_transaction(fx_transaction: FxTransactionBase):
    try:
        manager = FxTransactionManager(fx_transaction)
        return await manager.create_fx_transaction()
    except Exception as e:
        raise e


@router.get("/fx-transactions")
async def get_fx_transactions():
    try:
        manager = FxTransactionManager()
        return await manager.get_fx_transactions()
    except Exception as e:
        raise e


@router.get("/fx-transactions/{fx_transaction_id}")
async def get_fx_transaction_by_id(fx_transaction_id: int):
    try:
        manager = FxTransactionManager()
        return await manager.get_fx_transaction(fx_transaction_id)
    except Exception as e:
        raise e


@router.patch("/fx-transactions/{fx_transaction_id}")
async def update_fx_transaction(fx_transaction_id: int, fx_transaction: FxTransactionBase):
    try:
        manager = FxTransactionManager(fx_transaction)
        return await manager.update_fx_transaction(fx_transaction_id)
    except Exception as e:
        raise e


@router.delete("/fx-transactions/{fx_transaction_id}")
async def delete_fx_transaction(fx_transaction_id: int):
    try:
        manager = FxTransactionManager()
        return await manager.delete_fx_transaction(fx_transaction_id)
    except Exception as e:
        raise e


@router.post("/fx-transactions/{fx_transaction_id}/book")
async def book_fx_transaction(fx_transaction_id: int):
    try:
        manager = FxTransactionManager()
        return await manager.book_fx_transaction(fx_transaction_id)
    except Exception as e:
        raise e


@router.post("/fx-transactions/{fx_transaction_id}/settle")
async def settle_fx_transaction(fx_transaction_id: int):
    try:
        manager = FxTransactionManager()
        return await manager.settle_fx_transaction(fx_transaction_id)
    except Exception as e:
        raise e


@router.post("/fx-transactions/{fx_transaction_id}/cancel")
async def cancel_fx_transaction(fx_transaction_id: int):
    try:
        manager = FxTransactionManager()
        return await manager.cancel_fx_transaction(fx_transaction_id)
    except Exception as e:
        raise e


# ============================================================
# Bank Statement Lines
# ============================================================

@router.post("/bank-statement-lines")
async def create_bank_statement_line(statement_line: BankStatementLineBase):
    try:
        manager = BankStatementLineManager(statement_line)
        return await manager.create_bank_statement_line()
    except Exception as e:
        raise e


@router.get("/bank-statement-lines")
async def get_bank_statement_lines():
    try:
        manager = BankStatementLineManager()
        return await manager.get_bank_statement_lines()
    except Exception as e:
        raise e


@router.get("/bank-statement-lines/{statement_line_id}")
async def get_bank_statement_line_by_id(statement_line_id: int):
    try:
        manager = BankStatementLineManager()
        return await manager.get_bank_statement_line(statement_line_id)
    except Exception as e:
        raise e


@router.patch("/bank-statement-lines/{statement_line_id}")
async def update_bank_statement_line(statement_line_id: int, statement_line: BankStatementLineBase):
    try:
        manager = BankStatementLineManager(statement_line)
        return await manager.update_bank_statement_line(statement_line_id)
    except Exception as e:
        raise e


@router.delete("/bank-statement-lines/{statement_line_id}")
async def delete_bank_statement_line(statement_line_id: int):
    try:
        manager = BankStatementLineManager()
        return await manager.delete_bank_statement_line(statement_line_id)
    except Exception as e:
        raise e


# ============================================================
# Reconciliation
# ============================================================

@router.post("/reconciliations")
async def create_reconciliation(reconciliation: ReconciliationBase):
    try:
        manager = ReconciliationManager(reconciliation)
        return await manager.create_reconciliation()
    except Exception as e:
        raise e


@router.get("/reconciliations")
async def get_reconciliations():
    try:
        manager = ReconciliationManager()
        return await manager.get_reconciliations()
    except Exception as e:
        raise e


@router.post("/reconciliations/match")
async def match_transaction_to_statement_line(match: ReconciliationMatchBase):
    try:
        manager = ReconciliationManager()
        return await manager.match_transaction_to_statement_line(match)
    except Exception as e:
        raise e


@router.post("/reconciliations/unmatch")
async def unmatch_transaction_from_statement_line(match: ReconciliationMatchBase):
    try:
        manager = ReconciliationManager()
        return await manager.unmatch_transaction_from_statement_line(match)
    except Exception as e:
        raise e


@router.get("/reconciliations/{reconciliation_id}")
async def get_reconciliation_by_id(reconciliation_id: int):
    try:
        manager = ReconciliationManager()
        return await manager.get_reconciliation(reconciliation_id)
    except Exception as e:
        raise e


@router.patch("/reconciliations/{reconciliation_id}")
async def update_reconciliation(reconciliation_id: int, reconciliation: ReconciliationBase):
    try:
        manager = ReconciliationManager(reconciliation)
        return await manager.update_reconciliation(reconciliation_id)
    except Exception as e:
        raise e


@router.delete("/reconciliations/{reconciliation_id}")
async def delete_reconciliation(reconciliation_id: int):
    try:
        manager = ReconciliationManager()
        return await manager.delete_reconciliation(reconciliation_id)
    except Exception as e:
        raise e


# ============================================================
# Cash Balance Snapshots
# ============================================================

@router.post("/cash-balance-snapshots")
async def create_cash_balance_snapshot(snapshot: CashBalanceSnapshotBase):
    try:
        manager = CashBalanceSnapshotManager(snapshot)
        return await manager.create_cash_balance_snapshot()
    except Exception as e:
        raise e


@router.get("/cash-balance-snapshots")
async def get_cash_balance_snapshots():
    try:
        manager = CashBalanceSnapshotManager()
        return await manager.get_cash_balance_snapshots()
    except Exception as e:
        raise e


@router.get("/companies/{company_id}/cash-balance-snapshots")
async def get_cash_balance_snapshots_by_company(company_id: int):
    try:
        manager = CashBalanceSnapshotManager()
        return await manager.get_cash_balance_snapshots_by_company(company_id)
    except Exception as e:
        raise e


# ============================================================
# Treasury Dashboard / Summaries
# ============================================================

@router.get("/summary/cash-by-company")
async def get_cash_summary_by_company():
    try:
        manager = TreasurySummaryManager()
        return await manager.get_cash_summary_by_company()
    except Exception as e:
        raise e


@router.get("/summary/cash-by-currency")
async def get_cash_summary_by_currency():
    try:
        manager = TreasurySummaryManager()
        return await manager.get_cash_summary_by_currency()
    except Exception as e:
        raise e


@router.get("/summary/upcoming-payables")
async def get_upcoming_payables():
    try:
        manager = TreasurySummaryManager()
        return await manager.get_upcoming_payables()
    except Exception as e:
        raise e


@router.get("/summary/upcoming-receivables")
async def get_upcoming_receivables():
    try:
        manager = TreasurySummaryManager()
        return await manager.get_upcoming_receivables()
    except Exception as e:
        raise e


@router.get("/summary/projected-cashflow")
async def get_projected_cashflow():
    try:
        manager = TreasurySummaryManager()
        return await manager.get_projected_cashflow()
    except Exception as e:
        raise e


@router.get("/summary/trade-cashflow/{trade_id}")
async def get_trade_cashflow_summary(trade_id: int):
    try:
        manager = TreasurySummaryManager()
        return await manager.get_trade_cashflow_summary(trade_id)
    except Exception as e:
        raise e
