# app/treasury/managers.py

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
    PayableStatus,
    ReceivableStatus,
    ExpenseStatus,
    ReimbursementStatus,
    FxTransactionStatus,
)
from app.treasury.db import (
    get_accounts_db,
    get_account_db,
    get_accounts_by_company_db,
    get_account_balance_db,
    add_account_db,
    update_account_db,
    delete_account_db,
    get_transactions_db,
    get_transaction_db,
    get_transactions_by_account_db,
    get_transactions_by_trade_db,
    get_transactions_by_shipment_db,
    add_transaction_db,
    update_transaction_db,
    delete_transaction_db,
    complete_transaction_db,
    cancel_transaction_db,
    reconcile_transaction_db,
    get_payables_db,
    get_payable_db,
    get_payables_by_trade_db,
    get_payables_by_counterparty_db,
    add_payable_db,
    update_payable_db,
    delete_payable_db,
    update_payable_status_db,
    mark_payable_as_paid_db,
    get_receivables_db,
    get_receivable_db,
    get_receivables_by_trade_db,
    get_receivables_by_counterparty_db,
    add_receivable_db,
    update_receivable_db,
    delete_receivable_db,
    update_receivable_status_db,
    mark_receivable_as_received_db,
    get_transfers_db,
    get_transfer_db,
    add_transfer_db,
    update_transfer_db,
    delete_transfer_db,
    complete_transfer_db,
    cancel_transfer_db,
    get_expenses_db,
    get_expense_db,
    get_expenses_by_company_db,
    get_expenses_by_trade_db,
    get_expenses_by_shipment_db,
    get_expenses_by_month_year_db,
    get_expense_total_by_month_year_db,
    get_monthly_expense_totals_db,
    get_expenses_by_account_month_year_db,
    get_expense_total_by_account_month_year_db,
    get_monthly_expense_totals_by_account_db,
    get_expenses_by_user_month_year_db,
    get_expense_total_by_user_month_year_db,
    get_monthly_expense_totals_by_user_db,
    add_expense_db,
    update_expense_db,
    delete_expense_db,
    update_expense_status_db,
    mark_expense_as_paid_db,
    get_reimbursements_db,
    get_reimbursement_db,
    get_reimbursements_by_user_db,
    add_reimbursement_db,
    update_reimbursement_db,
    delete_reimbursement_db,
    update_reimbursement_status_db,
    mark_reimbursement_as_reimbursed_db,
    get_fx_transactions_db,
    get_fx_transaction_db,
    add_fx_transaction_db,
    update_fx_transaction_db,
    delete_fx_transaction_db,
    update_fx_transaction_status_db,
    settle_fx_transaction_db,
    get_bank_statement_lines_db,
    get_bank_statement_line_db,
    get_bank_statement_lines_by_account_db,
    add_bank_statement_line_db,
    update_bank_statement_line_db,
    delete_bank_statement_line_db,
    get_reconciliations_db,
    get_reconciliation_db,
    add_reconciliation_db,
    update_reconciliation_db,
    delete_reconciliation_db,
    match_transaction_to_statement_line_db,
    unmatch_transaction_from_statement_line_db,
    get_cash_balance_snapshots_db,
    get_cash_balance_snapshots_by_account_db,
    get_cash_balance_snapshots_by_company_db,
    add_cash_balance_snapshot_db,
    get_cash_summary_by_company_db,
    get_cash_summary_by_currency_db,
    get_upcoming_payables_db,
    get_upcoming_receivables_db,
    get_projected_cashflow_db,
    get_trade_cashflow_summary_db,
)


class AccountManager:
    def __init__(self, account: AccountBase = None):
        self.account = account

    async def get_accounts(self):
        return await get_accounts_db()

    async def get_account(self, account_id: int):
        return await get_account_db(account_id)

    async def get_accounts_by_company(self, company_id: int):
        return await get_accounts_by_company_db(company_id)

    async def get_account_balance(self, account_id: int):
        return await get_account_balance_db(account_id)

    async def create_account(self):
        return await add_account_db(self.account)

    async def update_account(self, account_id: int):
        return await update_account_db(self.account, account_id)

    async def delete_account(self, account_id: int):
        return await delete_account_db(account_id)

    async def get_expenses_by_month_year(self, account_id: int, month: int, year: int):
        return await get_expenses_by_account_month_year_db(account_id, month, year)

    async def get_expense_total_by_month_year(self, account_id: int, month: int, year: int):
        return await get_expense_total_by_account_month_year_db(account_id, month, year)

    async def get_monthly_expense_totals(self, account_id: int):
        return await get_monthly_expense_totals_by_account_db(account_id)


class TreasuryTransactionManager:
    def __init__(self, transaction: TreasuryTransactionBase = None):
        self.transaction = transaction

    async def get_transactions(self):
        return await get_transactions_db()

    async def get_transaction(self, transaction_id: int):
        return await get_transaction_db(transaction_id)

    async def get_transactions_by_account(self, account_id: int):
        return await get_transactions_by_account_db(account_id)

    async def get_transactions_by_trade(self, trade_id: int):
        return await get_transactions_by_trade_db(trade_id)

    async def get_transactions_by_shipment(self, shipment_id: int):
        return await get_transactions_by_shipment_db(shipment_id)

    async def create_transaction(self):
        return await add_transaction_db(self.transaction)

    async def update_transaction(self, transaction_id: int):
        return await update_transaction_db(self.transaction, transaction_id)

    async def delete_transaction(self, transaction_id: int):
        return await delete_transaction_db(transaction_id)

    async def complete_transaction(self, transaction_id: int):
        return await complete_transaction_db(transaction_id)

    async def cancel_transaction(self, transaction_id: int):
        return await cancel_transaction_db(transaction_id)

    async def reconcile_transaction(self, transaction_id: int):
        return await reconcile_transaction_db(transaction_id)


class PayableManager:
    def __init__(self, payable: PayableBase = None):
        self.payable = payable

    async def get_payables(self):
        return await get_payables_db()

    async def get_payable(self, payable_id: int):
        return await get_payable_db(payable_id)

    async def get_payables_by_trade(self, trade_id: int):
        return await get_payables_by_trade_db(trade_id)

    async def get_payables_by_counterparty(self, counterparty_id: int):
        return await get_payables_by_counterparty_db(counterparty_id)

    async def create_payable(self):
        return await add_payable_db(self.payable)

    async def update_payable(self, payable_id: int):
        return await update_payable_db(self.payable, payable_id)

    async def delete_payable(self, payable_id: int):
        return await delete_payable_db(payable_id)

    async def approve_payable(self, payable_id: int):
        return await update_payable_status_db(payable_id, PayableStatus.APPROVED)

    async def schedule_payable(self, payable_id: int):
        return await update_payable_status_db(payable_id, PayableStatus.SCHEDULED)

    async def mark_payable_as_paid(self, payable_id: int):
        return await mark_payable_as_paid_db(payable_id)

    async def cancel_payable(self, payable_id: int):
        return await update_payable_status_db(payable_id, PayableStatus.CANCELLED)


class ReceivableManager:
    def __init__(self, receivable: ReceivableBase = None):
        self.receivable = receivable

    async def get_receivables(self):
        return await get_receivables_db()

    async def get_receivable(self, receivable_id: int):
        return await get_receivable_db(receivable_id)

    async def get_receivables_by_trade(self, trade_id: int):
        return await get_receivables_by_trade_db(trade_id)

    async def get_receivables_by_counterparty(self, counterparty_id: int):
        return await get_receivables_by_counterparty_db(counterparty_id)

    async def create_receivable(self):
        return await add_receivable_db(self.receivable)

    async def update_receivable(self, receivable_id: int):
        return await update_receivable_db(self.receivable, receivable_id)

    async def delete_receivable(self, receivable_id: int):
        return await delete_receivable_db(receivable_id)

    async def mark_receivable_as_invoiced(self, receivable_id: int):
        return await update_receivable_status_db(receivable_id, ReceivableStatus.INVOICED)

    async def mark_receivable_as_received(self, receivable_id: int):
        return await mark_receivable_as_received_db(receivable_id)

    async def cancel_receivable(self, receivable_id: int):
        return await update_receivable_status_db(receivable_id, ReceivableStatus.CANCELLED)


class AccountTransferManager:
    def __init__(self, transfer: AccountTransferBase = None):
        self.transfer = transfer

    async def get_transfers(self):
        return await get_transfers_db()

    async def get_transfer(self, transfer_id: int):
        return await get_transfer_db(transfer_id)

    async def create_transfer(self):
        return await add_transfer_db(self.transfer)

    async def update_transfer(self, transfer_id: int):
        return await update_transfer_db(self.transfer, transfer_id)

    async def delete_transfer(self, transfer_id: int):
        return await delete_transfer_db(transfer_id)

    async def complete_transfer(self, transfer_id: int):
        return await complete_transfer_db(transfer_id)

    async def cancel_transfer(self, transfer_id: int):
        return await cancel_transfer_db(transfer_id)


class ExpenseManager:
    def __init__(self, expense: ExpenseBase = None):
        self.expense = expense

    async def get_expenses(self):
        return await get_expenses_db()

    async def get_expense(self, expense_id: int):
        return await get_expense_db(expense_id)

    async def get_expenses_by_company(self, company_id: int):
        return await get_expenses_by_company_db(company_id)

    async def get_expenses_by_trade(self, trade_id: int):
        return await get_expenses_by_trade_db(trade_id)

    async def get_expenses_by_shipment(self, shipment_id: int):
        return await get_expenses_by_shipment_db(shipment_id)

    async def get_expenses_by_month_year(self, month: int, year: int):
        return await get_expenses_by_month_year_db(month, year)

    async def get_expense_total_by_month_year(self, month: int, year: int):
        return await get_expense_total_by_month_year_db(month, year)

    async def get_monthly_expense_totals(self):
        return await get_monthly_expense_totals_db()

    async def get_expenses_by_user_month_year(self, user_id: int, month: int, year: int):
        return await get_expenses_by_user_month_year_db(user_id, month, year)

    async def get_expense_total_by_user_month_year(self, user_id: int, month: int, year: int):
        return await get_expense_total_by_user_month_year_db(user_id, month, year)

    async def get_monthly_expense_totals_by_user(self, user_id: int):
        return await get_monthly_expense_totals_by_user_db(user_id)

    async def create_expense(self):
        return await add_expense_db(self.expense)

    async def update_expense(self, expense_id: int):
        return await update_expense_db(self.expense, expense_id)

    async def delete_expense(self, expense_id: int):
        return await delete_expense_db(expense_id)

    async def submit_expense(self, expense_id: int):
        return await update_expense_status_db(expense_id, ExpenseStatus.SUBMITTED)

    async def approve_expense(self, expense_id: int):
        return await update_expense_status_db(expense_id, ExpenseStatus.APPROVED)

    async def reject_expense(self, expense_id: int):
        return await update_expense_status_db(expense_id, ExpenseStatus.REJECTED)

    async def mark_expense_as_paid(self, expense_id: int):
        return await mark_expense_as_paid_db(expense_id)


class ReimbursementManager:
    def __init__(self, reimbursement: ReimbursementBase = None):
        self.reimbursement = reimbursement

    async def get_reimbursements(self):
        return await get_reimbursements_db()

    async def get_reimbursement(self, reimbursement_id: int):
        return await get_reimbursement_db(reimbursement_id)

    async def get_reimbursements_by_user(self, user_id: int):
        return await get_reimbursements_by_user_db(user_id)

    async def create_reimbursement(self):
        return await add_reimbursement_db(self.reimbursement)

    async def update_reimbursement(self, reimbursement_id: int):
        return await update_reimbursement_db(self.reimbursement, reimbursement_id)

    async def delete_reimbursement(self, reimbursement_id: int):
        return await delete_reimbursement_db(reimbursement_id)

    async def approve_reimbursement(self, reimbursement_id: int):
        return await update_reimbursement_status_db(reimbursement_id, ReimbursementStatus.APPROVED)

    async def reject_reimbursement(self, reimbursement_id: int):
        return await update_reimbursement_status_db(reimbursement_id, ReimbursementStatus.REJECTED)

    async def mark_reimbursement_as_reimbursed(self, reimbursement_id: int):
        return await mark_reimbursement_as_reimbursed_db(reimbursement_id)


class FxTransactionManager:
    def __init__(self, fx_transaction: FxTransactionBase = None):
        self.fx_transaction = fx_transaction

    async def get_fx_transactions(self):
        return await get_fx_transactions_db()

    async def get_fx_transaction(self, fx_transaction_id: int):
        return await get_fx_transaction_db(fx_transaction_id)

    async def create_fx_transaction(self):
        return await add_fx_transaction_db(self.fx_transaction)

    async def update_fx_transaction(self, fx_transaction_id: int):
        return await update_fx_transaction_db(self.fx_transaction, fx_transaction_id)

    async def delete_fx_transaction(self, fx_transaction_id: int):
        return await delete_fx_transaction_db(fx_transaction_id)

    async def book_fx_transaction(self, fx_transaction_id: int):
        return await update_fx_transaction_status_db(fx_transaction_id, FxTransactionStatus.BOOKED)

    async def settle_fx_transaction(self, fx_transaction_id: int):
        return await settle_fx_transaction_db(fx_transaction_id)

    async def cancel_fx_transaction(self, fx_transaction_id: int):
        return await update_fx_transaction_status_db(fx_transaction_id, FxTransactionStatus.CANCELLED)


class BankStatementLineManager:
    def __init__(self, statement_line: BankStatementLineBase = None):
        self.statement_line = statement_line

    async def get_bank_statement_lines(self):
        return await get_bank_statement_lines_db()

    async def get_bank_statement_line(self, statement_line_id: int):
        return await get_bank_statement_line_db(statement_line_id)

    async def get_bank_statement_lines_by_account(self, account_id: int):
        return await get_bank_statement_lines_by_account_db(account_id)

    async def create_bank_statement_line(self):
        return await add_bank_statement_line_db(self.statement_line)

    async def update_bank_statement_line(self, statement_line_id: int):
        return await update_bank_statement_line_db(self.statement_line, statement_line_id)

    async def delete_bank_statement_line(self, statement_line_id: int):
        return await delete_bank_statement_line_db(statement_line_id)


class ReconciliationManager:
    def __init__(self, reconciliation: ReconciliationBase = None):
        self.reconciliation = reconciliation

    async def get_reconciliations(self):
        return await get_reconciliations_db()

    async def get_reconciliation(self, reconciliation_id: int):
        return await get_reconciliation_db(reconciliation_id)

    async def create_reconciliation(self):
        return await add_reconciliation_db(self.reconciliation)

    async def update_reconciliation(self, reconciliation_id: int):
        return await update_reconciliation_db(self.reconciliation, reconciliation_id)

    async def delete_reconciliation(self, reconciliation_id: int):
        return await delete_reconciliation_db(reconciliation_id)

    async def match_transaction_to_statement_line(self, match: ReconciliationMatchBase):
        return await match_transaction_to_statement_line_db(match)

    async def unmatch_transaction_from_statement_line(self, match: ReconciliationMatchBase):
        return await unmatch_transaction_from_statement_line_db(match)


class CashBalanceSnapshotManager:
    def __init__(self, snapshot: CashBalanceSnapshotBase = None):
        self.snapshot = snapshot

    async def get_cash_balance_snapshots(self):
        return await get_cash_balance_snapshots_db()

    async def get_cash_balance_snapshots_by_account(self, account_id: int):
        return await get_cash_balance_snapshots_by_account_db(account_id)

    async def get_cash_balance_snapshots_by_company(self, company_id: int):
        return await get_cash_balance_snapshots_by_company_db(company_id)

    async def create_cash_balance_snapshot(self):
        return await add_cash_balance_snapshot_db(self.snapshot)


class TreasurySummaryManager:
    async def get_cash_summary_by_company(self):
        return await get_cash_summary_by_company_db()

    async def get_cash_summary_by_currency(self):
        return await get_cash_summary_by_currency_db()

    async def get_upcoming_payables(self):
        return await get_upcoming_payables_db()

    async def get_upcoming_receivables(self):
        return await get_upcoming_receivables_db()

    async def get_projected_cashflow(self):
        return await get_projected_cashflow_db()

    async def get_trade_cashflow_summary(self, trade_id: int):
        return await get_trade_cashflow_summary_db(trade_id)
