# app/treasury/db.py

import calendar
from collections import defaultdict
from datetime import date
from decimal import Decimal

from app.connection import supabase
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
    TransactionType,
    TransactionStatus,
    PayableStatus,
    ReceivableStatus,
    TransferStatus,
    ExpenseStatus,
    ReimbursementStatus,
    FxTransactionStatus,
    ReconciliationStatus,
)


def _to_float(value) -> float:
    if value is None:
        return 0.0
    if isinstance(value, Decimal):
        return float(value)
    return float(value)


def _serialize(model) -> dict:
    return model.model_dump(mode="json")


# Account DB Operations

async def get_accounts_db():
    response = supabase.table("accounts").select("*").execute()
    return response.data

async def get_account_db(account_id: int):
    response = supabase.table("accounts").select("*").eq("id", account_id).execute()
    return response.data

async def get_accounts_by_company_db(company_id: int):
    response = supabase.table("accounts").select("*").eq("company_id", company_id).execute()
    return response.data

async def get_account_balance_db(account_id: int):
    response = supabase.table("accounts").select("id, current_balance, currency").eq("id", account_id).execute()
    if not response.data:
        return None
    account = response.data[0]
    return {
        "account_id": account_id,
        "current_balance": account.get("current_balance"),
        "currency": account.get("currency"),
    }

async def add_account_db(account: AccountBase):
    account_data = _serialize(account)
    response = supabase.table("accounts").insert(account_data).execute()
    return response.data

async def update_account_db(account: AccountBase, account_id: int):
    account_data = account.model_dump(mode="json", exclude_unset=True)
    response = supabase.table("accounts").update(account_data).eq("id", account_id).execute()
    return response.data

async def delete_account_db(account_id: int):
    response = supabase.table("accounts").delete().eq("id", account_id).execute()
    return response.data

async def adjust_account_balance_db(account_id: int, amount):
    response = supabase.table("accounts").select("current_balance").eq("id", account_id).execute()
    if not response.data:
        return None
    current_balance = _to_float(response.data[0].get("current_balance"))
    new_balance = current_balance + _to_float(amount)
    response = supabase.table("accounts").update({"current_balance": new_balance}).eq("id", account_id).execute()
    return response.data


# Treasury Transaction DB Operations

async def get_transactions_db():
    response = supabase.table("treasury_transactions").select("*").execute()
    return response.data

async def get_transaction_db(transaction_id: int):
    response = supabase.table("treasury_transactions").select("*").eq("id", transaction_id).execute()
    return response.data

async def get_transactions_by_account_db(account_id: int):
    response = supabase.table("treasury_transactions").select("*").eq("account_id", account_id).execute()
    return response.data

async def get_transactions_by_trade_db(trade_id: int):
    response = supabase.table("treasury_transactions").select("*").eq("trade_id", trade_id).execute()
    return response.data

async def get_transactions_by_shipment_db(shipment_id: int):
    response = supabase.table("treasury_transactions").select("*").eq("shipment_id", shipment_id).execute()
    return response.data

async def add_transaction_db(transaction: TreasuryTransactionBase):
    transaction_data = _serialize(transaction)
    response = supabase.table("treasury_transactions").insert(transaction_data).execute()
    return response.data

async def update_transaction_db(transaction: TreasuryTransactionBase, transaction_id: int):
    transaction_data = transaction.model_dump(mode="json", exclude_unset=True)
    response = supabase.table("treasury_transactions").update(transaction_data).eq("id", transaction_id).execute()
    return response.data

async def delete_transaction_db(transaction_id: int):
    response = supabase.table("treasury_transactions").delete().eq("id", transaction_id).execute()
    return response.data

async def _apply_transaction_balance_effect(transaction: dict):
    account_id = transaction.get("account_id")
    amount = transaction.get("amount")
    transaction_type = transaction.get("transaction_type")
    if not account_id or amount is None:
        return
    if transaction_type == TransactionType.INFLOW.value:
        await adjust_account_balance_db(account_id, amount)
    elif transaction_type == TransactionType.OUTFLOW.value:
        await adjust_account_balance_db(account_id, -_to_float(amount))
    elif transaction_type == TransactionType.ADJUSTMENT.value:
        await adjust_account_balance_db(account_id, amount)

async def _reverse_transaction_balance_effect(transaction: dict):
    account_id = transaction.get("account_id")
    amount = transaction.get("amount")
    transaction_type = transaction.get("transaction_type")
    if not account_id or amount is None:
        return
    if transaction_type == TransactionType.INFLOW.value:
        await adjust_account_balance_db(account_id, -_to_float(amount))
    elif transaction_type == TransactionType.OUTFLOW.value:
        await adjust_account_balance_db(account_id, amount)
    elif transaction_type == TransactionType.ADJUSTMENT.value:
        await adjust_account_balance_db(account_id, -_to_float(amount))

async def complete_transaction_db(transaction_id: int):
    response = supabase.table("treasury_transactions").select("*").eq("id", transaction_id).execute()
    if not response.data:
        return None
    transaction = response.data[0]
    if transaction.get("status") == TransactionStatus.COMPLETED.value:
        return response.data
    await _apply_transaction_balance_effect(transaction)
    response = (
        supabase.table("treasury_transactions")
        .update({"status": TransactionStatus.COMPLETED.value})
        .eq("id", transaction_id)
        .execute()
    )
    return response.data

async def cancel_transaction_db(transaction_id: int):
    response = supabase.table("treasury_transactions").select("*").eq("id", transaction_id).execute()
    if not response.data:
        return None
    transaction = response.data[0]
    if transaction.get("status") == TransactionStatus.COMPLETED.value:
        await _reverse_transaction_balance_effect(transaction)
    response = (
        supabase.table("treasury_transactions")
        .update({"status": TransactionStatus.CANCELLED.value})
        .eq("id", transaction_id)
        .execute()
    )
    return response.data

async def reconcile_transaction_db(transaction_id: int):
    response = (
        supabase.table("treasury_transactions")
        .update({"status": TransactionStatus.RECONCILED.value})
        .eq("id", transaction_id)
        .execute()
    )
    return response.data


# Payable DB Operations

async def get_payables_db():
    response = supabase.table("payables").select("*").execute()
    return response.data

async def get_payable_db(payable_id: int):
    response = supabase.table("payables").select("*").eq("id", payable_id).execute()
    return response.data

async def get_payables_by_trade_db(trade_id: int):
    response = supabase.table("payables").select("*").eq("trade_id", trade_id).execute()
    return response.data

async def get_payables_by_counterparty_db(counterparty_id: int):
    response = supabase.table("payables").select("*").eq("counterparty_id", counterparty_id).execute()
    return response.data

async def add_payable_db(payable: PayableBase):
    payable_data = _serialize(payable)
    if payable_data.get("remaining_amount") is None and payable.amount is not None:
        payable_data["remaining_amount"] = str(payable.amount)
    response = supabase.table("payables").insert(payable_data).execute()
    return response.data

async def update_payable_db(payable: PayableBase, payable_id: int):
    payable_data = payable.model_dump(mode="json", exclude_unset=True)
    response = supabase.table("payables").update(payable_data).eq("id", payable_id).execute()
    return response.data

async def delete_payable_db(payable_id: int):
    response = supabase.table("payables").delete().eq("id", payable_id).execute()
    return response.data

async def update_payable_status_db(payable_id: int, status: PayableStatus, **extra_fields):
    update_data = {"status": status.value, **extra_fields}
    response = supabase.table("payables").update(update_data).eq("id", payable_id).execute()
    return response.data

async def mark_payable_as_paid_db(payable_id: int):
    response = supabase.table("payables").select("*").eq("id", payable_id).execute()
    if not response.data:
        return None
    payable = response.data[0]
    amount = payable.get("amount")
    return await update_payable_status_db(
        payable_id,
        PayableStatus.PAID,
        amount_paid=amount,
        remaining_amount=0,
    )


# Receivable DB Operations

async def get_receivables_db():
    response = supabase.table("receivables").select("*").execute()
    return response.data

async def get_receivable_db(receivable_id: int):
    response = supabase.table("receivables").select("*").eq("id", receivable_id).execute()
    return response.data

async def get_receivables_by_trade_db(trade_id: int):
    response = supabase.table("receivables").select("*").eq("trade_id", trade_id).execute()
    return response.data

async def get_receivables_by_counterparty_db(counterparty_id: int):
    response = supabase.table("receivables").select("*").eq("counterparty_id", counterparty_id).execute()
    return response.data

async def add_receivable_db(receivable: ReceivableBase):
    receivable_data = _serialize(receivable)
    if receivable_data.get("remaining_amount") is None and receivable.amount is not None:
        receivable_data["remaining_amount"] = str(receivable.amount)
    response = supabase.table("receivables").insert(receivable_data).execute()
    return response.data

async def update_receivable_db(receivable: ReceivableBase, receivable_id: int):
    receivable_data = receivable.model_dump(mode="json", exclude_unset=True)
    response = supabase.table("receivables").update(receivable_data).eq("id", receivable_id).execute()
    return response.data

async def delete_receivable_db(receivable_id: int):
    response = supabase.table("receivables").delete().eq("id", receivable_id).execute()
    return response.data

async def update_receivable_status_db(receivable_id: int, status: ReceivableStatus, **extra_fields):
    update_data = {"status": status.value, **extra_fields}
    response = supabase.table("receivables").update(update_data).eq("id", receivable_id).execute()
    return response.data

async def mark_receivable_as_received_db(receivable_id: int):
    response = supabase.table("receivables").select("*").eq("id", receivable_id).execute()
    if not response.data:
        return None
    receivable = response.data[0]
    amount = receivable.get("amount")
    return await update_receivable_status_db(
        receivable_id,
        ReceivableStatus.RECEIVED,
        amount_received=amount,
        remaining_amount=0,
    )


# Account Transfer DB Operations

async def get_transfers_db():
    response = supabase.table("account_transfers").select("*").execute()
    return response.data

async def get_transfer_db(transfer_id: int):
    response = supabase.table("account_transfers").select("*").eq("id", transfer_id).execute()
    return response.data

async def add_transfer_db(transfer: AccountTransferBase):
    transfer_data = _serialize(transfer)
    response = supabase.table("account_transfers").insert(transfer_data).execute()
    return response.data

async def update_transfer_db(transfer: AccountTransferBase, transfer_id: int):
    transfer_data = transfer.model_dump(mode="json", exclude_unset=True)
    response = supabase.table("account_transfers").update(transfer_data).eq("id", transfer_id).execute()
    return response.data

async def delete_transfer_db(transfer_id: int):
    response = supabase.table("account_transfers").delete().eq("id", transfer_id).execute()
    return response.data

async def complete_transfer_db(transfer_id: int):
    response = supabase.table("account_transfers").select("*").eq("id", transfer_id).execute()
    if not response.data:
        return None
    transfer = response.data[0]
    if transfer.get("status") == TransferStatus.COMPLETED.value:
        return response.data
    await adjust_account_balance_db(transfer["from_account_id"], -_to_float(transfer["amount"]))
    await adjust_account_balance_db(transfer["to_account_id"], transfer["amount"])
    response = (
        supabase.table("account_transfers")
        .update({"status": TransferStatus.COMPLETED.value})
        .eq("id", transfer_id)
        .execute()
    )
    return response.data

async def cancel_transfer_db(transfer_id: int):
    response = supabase.table("account_transfers").select("*").eq("id", transfer_id).execute()
    if not response.data:
        return None
    transfer = response.data[0]
    if transfer.get("status") == TransferStatus.COMPLETED.value:
        await adjust_account_balance_db(transfer["from_account_id"], transfer["amount"])
        await adjust_account_balance_db(transfer["to_account_id"], -_to_float(transfer["amount"]))
    response = (
        supabase.table("account_transfers")
        .update({"status": TransferStatus.CANCELLED.value})
        .eq("id", transfer_id)
        .execute()
    )
    return response.data


# Expense DB Operations

async def get_expenses_db():
    response = supabase.table("expenses").select("*").execute()
    return response.data

async def get_expense_db(expense_id: int):
    response = supabase.table("expenses").select("*").eq("id", expense_id).execute()
    return response.data

async def get_expenses_by_company_db(company_id: int):
    response = supabase.table("expenses").select("*").eq("company_id", company_id).execute()
    return response.data

async def get_expenses_by_trade_db(trade_id: int):
    response = supabase.table("expenses").select("*").eq("trade_id", trade_id).execute()
    return response.data

async def get_expenses_by_shipment_db(shipment_id: int):
    response = supabase.table("expenses").select("*").eq("shipment_id", shipment_id).execute()
    return response.data

async def get_expenses_by_month_year_db(month: int, year: int):
    start_date = date(year, month, 1)
    end_date = date(year, month, calendar.monthrange(year, month)[1])
    response = (
        supabase.table("expenses")
        .select("*")
        .gte("expense_date", start_date.isoformat())
        .lte("expense_date", end_date.isoformat())
        .execute()
    )
    return response.data

async def get_expense_total_by_month_year_db(month: int, year: int):
    start_date = date(year, month, 1)
    end_date = date(year, month, calendar.monthrange(year, month)[1])
    response = (
        supabase.table("expenses")
        .select("amount")
        .gte("expense_date", start_date.isoformat())
        .lte("expense_date", end_date.isoformat())
        .execute()
    )
    total = sum(_to_float(expense["amount"]) for expense in response.data if expense.get("amount") is not None)
    return {"year": year, "month": month, "total": total}

async def get_monthly_expense_totals_db():
    response = supabase.table("expenses").select("amount, expense_date").execute()
    totals = defaultdict(float)
    for expense in response.data:
        expense_date = expense.get("expense_date")
        amount = expense.get("amount")
        if not expense_date or amount is None:
            continue
        yr = int(expense_date[:4])
        mo = int(expense_date[5:7])
        totals[(yr, mo)] += _to_float(amount)
    return [
        {"year": yr, "month": mo, "total": total}
        for (yr, mo), total in sorted(totals.items(), reverse=True)
    ]

async def get_expenses_by_account_month_year_db(account_id: int, month: int, year: int):
    start_date = date(year, month, 1)
    end_date = date(year, month, calendar.monthrange(year, month)[1])
    response = (
        supabase.table("expenses")
        .select("*")
        .eq("account_id", account_id)
        .gte("expense_date", start_date.isoformat())
        .lte("expense_date", end_date.isoformat())
        .execute()
    )
    return response.data

async def get_expense_total_by_account_month_year_db(account_id: int, month: int, year: int):
    start_date = date(year, month, 1)
    end_date = date(year, month, calendar.monthrange(year, month)[1])
    response = (
        supabase.table("expenses")
        .select("amount")
        .eq("account_id", account_id)
        .gte("expense_date", start_date.isoformat())
        .lte("expense_date", end_date.isoformat())
        .execute()
    )
    total = sum(_to_float(expense["amount"]) for expense in response.data if expense.get("amount") is not None)
    return {"account_id": account_id, "year": year, "month": month, "total": total}

async def get_monthly_expense_totals_by_account_db(account_id: int):
    response = (
        supabase.table("expenses")
        .select("amount, expense_date")
        .eq("account_id", account_id)
        .execute()
    )
    totals = defaultdict(float)
    for expense in response.data:
        expense_date = expense.get("expense_date")
        amount = expense.get("amount")
        if not expense_date or amount is None:
            continue
        yr = int(expense_date[:4])
        mo = int(expense_date[5:7])
        totals[(yr, mo)] += _to_float(amount)
    return [
        {"account_id": account_id, "year": yr, "month": mo, "total": total}
        for (yr, mo), total in sorted(totals.items(), reverse=True)
    ]

async def _get_expense_ids_for_user_db(user_id: int):
    response = supabase.table("reimbursements").select("expense_id").eq("user_id", user_id).execute()
    return [reimbursement["expense_id"] for reimbursement in response.data if reimbursement.get("expense_id")]

async def get_expenses_by_user_month_year_db(user_id: int, month: int, year: int):
    expense_ids = await _get_expense_ids_for_user_db(user_id)
    if not expense_ids:
        return []
    start_date = date(year, month, 1)
    end_date = date(year, month, calendar.monthrange(year, month)[1])
    response = (
        supabase.table("expenses")
        .select("*")
        .in_("id", expense_ids)
        .gte("expense_date", start_date.isoformat())
        .lte("expense_date", end_date.isoformat())
        .execute()
    )
    return response.data

async def get_expense_total_by_user_month_year_db(user_id: int, month: int, year: int):
    expense_ids = await _get_expense_ids_for_user_db(user_id)
    if not expense_ids:
        return {"user_id": user_id, "year": year, "month": month, "total": 0}
    start_date = date(year, month, 1)
    end_date = date(year, month, calendar.monthrange(year, month)[1])
    response = (
        supabase.table("expenses")
        .select("amount")
        .in_("id", expense_ids)
        .gte("expense_date", start_date.isoformat())
        .lte("expense_date", end_date.isoformat())
        .execute()
    )
    total = sum(_to_float(expense["amount"]) for expense in response.data if expense.get("amount") is not None)
    return {"user_id": user_id, "year": year, "month": month, "total": total}

async def get_monthly_expense_totals_by_user_db(user_id: int):
    expense_ids = await _get_expense_ids_for_user_db(user_id)
    if not expense_ids:
        return []
    response = (
        supabase.table("expenses")
        .select("amount, expense_date")
        .in_("id", expense_ids)
        .execute()
    )
    totals = defaultdict(float)
    for expense in response.data:
        expense_date = expense.get("expense_date")
        amount = expense.get("amount")
        if not expense_date or amount is None:
            continue
        yr = int(expense_date[:4])
        mo = int(expense_date[5:7])
        totals[(yr, mo)] += _to_float(amount)
    return [
        {"user_id": user_id, "year": yr, "month": mo, "total": total}
        for (yr, mo), total in sorted(totals.items(), reverse=True)
    ]

async def add_expense_db(expense: ExpenseBase):
    expense_data = _serialize(expense)
    response = supabase.table("expenses").insert(expense_data).execute()
    return response.data

async def update_expense_db(expense: ExpenseBase, expense_id: int):
    expense_data = expense.model_dump(mode="json", exclude_unset=True)
    response = supabase.table("expenses").update(expense_data).eq("id", expense_id).execute()
    return response.data

async def delete_expense_db(expense_id: int):
    response = supabase.table("expenses").delete().eq("id", expense_id).execute()
    return response.data

async def update_expense_status_db(expense_id: int, status: ExpenseStatus):
    response = (
        supabase.table("expenses")
        .update({"status": status.value})
        .eq("id", expense_id)
        .execute()
    )
    return response.data

async def mark_expense_as_paid_db(expense_id: int):
    response = supabase.table("expenses").select("*").eq("id", expense_id).execute()
    if not response.data:
        return None
    expense = response.data[0]
    if not expense.get("is_reimbursement") and expense.get("account_id") and expense.get("amount"):
        await adjust_account_balance_db(expense["account_id"], -_to_float(expense["amount"]))
    response = (
        supabase.table("expenses")
        .update({"status": ExpenseStatus.PAID.value})
        .eq("id", expense_id)
        .execute()
    )
    return response.data


# Reimbursement DB Operations

async def get_reimbursements_db():
    response = supabase.table("reimbursements").select("*").execute()
    return response.data

async def get_reimbursement_db(reimbursement_id: int):
    response = supabase.table("reimbursements").select("*").eq("id", reimbursement_id).execute()
    return response.data

async def get_reimbursements_by_user_db(user_id: int):
    response = supabase.table("reimbursements").select("*").eq("user_id", user_id).execute()
    return response.data

async def add_reimbursement_db(reimbursement: ReimbursementBase):
    reimbursement_data = _serialize(reimbursement)
    response = supabase.table("reimbursements").insert(reimbursement_data).execute()
    return response.data

async def update_reimbursement_db(reimbursement: ReimbursementBase, reimbursement_id: int):
    reimbursement_data = reimbursement.model_dump(mode="json", exclude_unset=True)
    response = supabase.table("reimbursements").update(reimbursement_data).eq("id", reimbursement_id).execute()
    return response.data

async def delete_reimbursement_db(reimbursement_id: int):
    response = supabase.table("reimbursements").delete().eq("id", reimbursement_id).execute()
    return response.data

async def update_reimbursement_status_db(reimbursement_id: int, status: ReimbursementStatus):
    response = (
        supabase.table("reimbursements")
        .update({"status": status.value})
        .eq("id", reimbursement_id)
        .execute()
    )
    return response.data

async def mark_reimbursement_as_reimbursed_db(reimbursement_id: int):
    response = supabase.table("reimbursements").select("*").eq("id", reimbursement_id).execute()
    if not response.data:
        return None
    reimbursement = response.data[0]
    if reimbursement.get("status") == ReimbursementStatus.REIMBURSED.value:
        return response.data
    account_id = reimbursement.get("reimbursed_from_account_id")
    amount = reimbursement.get("amount")
    if not amount and reimbursement.get("expense_id"):
        expense_response = (
            supabase.table("expenses")
            .select("amount, account_id")
            .eq("id", reimbursement["expense_id"])
            .execute()
        )
        if expense_response.data:
            amount = expense_response.data[0].get("amount")
            if not account_id:
                account_id = expense_response.data[0].get("account_id")
    if account_id and amount:
        await adjust_account_balance_db(account_id, -_to_float(amount))
    response = (
        supabase.table("reimbursements")
        .update({"status": ReimbursementStatus.REIMBURSED.value})
        .eq("id", reimbursement_id)
        .execute()
    )
    return response.data


# FX Transaction DB Operations

async def get_fx_transactions_db():
    response = supabase.table("fx_transactions").select("*").execute()
    return response.data

async def get_fx_transaction_db(fx_transaction_id: int):
    response = supabase.table("fx_transactions").select("*").eq("id", fx_transaction_id).execute()
    return response.data

async def add_fx_transaction_db(fx_transaction: FxTransactionBase):
    fx_data = _serialize(fx_transaction)
    response = supabase.table("fx_transactions").insert(fx_data).execute()
    return response.data

async def update_fx_transaction_db(fx_transaction: FxTransactionBase, fx_transaction_id: int):
    fx_data = fx_transaction.model_dump(mode="json", exclude_unset=True)
    response = supabase.table("fx_transactions").update(fx_data).eq("id", fx_transaction_id).execute()
    return response.data

async def delete_fx_transaction_db(fx_transaction_id: int):
    response = supabase.table("fx_transactions").delete().eq("id", fx_transaction_id).execute()
    return response.data

async def update_fx_transaction_status_db(fx_transaction_id: int, status: FxTransactionStatus):
    response = (
        supabase.table("fx_transactions")
        .update({"status": status.value})
        .eq("id", fx_transaction_id)
        .execute()
    )
    return response.data

async def settle_fx_transaction_db(fx_transaction_id: int):
    response = supabase.table("fx_transactions").select("*").eq("id", fx_transaction_id).execute()
    if not response.data:
        return None
    fx = response.data[0]
    if fx.get("status") != FxTransactionStatus.SETTLED.value:
        await adjust_account_balance_db(fx["from_account_id"], -_to_float(fx["from_amount"]))
        await adjust_account_balance_db(fx["to_account_id"], fx["to_amount"])
        response = (
            supabase.table("fx_transactions")
            .update({"status": FxTransactionStatus.SETTLED.value})
            .eq("id", fx_transaction_id)
            .execute()
        )
    return response.data


# Bank Statement Line DB Operations

async def get_bank_statement_lines_db():
    response = supabase.table("bank_statement_lines").select("*").execute()
    return response.data

async def get_bank_statement_line_db(statement_line_id: int):
    response = supabase.table("bank_statement_lines").select("*").eq("id", statement_line_id).execute()
    return response.data

async def get_bank_statement_lines_by_account_db(account_id: int):
    response = supabase.table("bank_statement_lines").select("*").eq("account_id", account_id).execute()
    return response.data

async def add_bank_statement_line_db(statement_line: BankStatementLineBase):
    line_data = _serialize(statement_line)
    response = supabase.table("bank_statement_lines").insert(line_data).execute()
    return response.data

async def update_bank_statement_line_db(statement_line: BankStatementLineBase, statement_line_id: int):
    line_data = statement_line.model_dump(mode="json", exclude_unset=True)
    response = supabase.table("bank_statement_lines").update(line_data).eq("id", statement_line_id).execute()
    return response.data

async def delete_bank_statement_line_db(statement_line_id: int):
    response = supabase.table("bank_statement_lines").delete().eq("id", statement_line_id).execute()
    return response.data


# Reconciliation DB Operations

async def get_reconciliations_db():
    response = supabase.table("reconciliations").select("*").execute()
    return response.data

async def get_reconciliation_db(reconciliation_id: int):
    response = supabase.table("reconciliations").select("*").eq("id", reconciliation_id).execute()
    return response.data

async def add_reconciliation_db(reconciliation: ReconciliationBase):
    reconciliation_data = _serialize(reconciliation)
    response = supabase.table("reconciliations").insert(reconciliation_data).execute()
    return response.data

async def update_reconciliation_db(reconciliation: ReconciliationBase, reconciliation_id: int):
    reconciliation_data = reconciliation.model_dump(mode="json", exclude_unset=True)
    response = supabase.table("reconciliations").update(reconciliation_data).eq("id", reconciliation_id).execute()
    return response.data

async def delete_reconciliation_db(reconciliation_id: int):
    response = supabase.table("reconciliations").delete().eq("id", reconciliation_id).execute()
    return response.data

async def match_transaction_to_statement_line_db(match: ReconciliationMatchBase):
    response = (
        supabase.table("bank_statement_lines")
        .update({
            "is_matched": True,
            "treasury_transaction_id": match.treasury_transaction_id,
        })
        .eq("id", match.bank_statement_line_id)
        .execute()
    )
    await reconcile_transaction_db(match.treasury_transaction_id)
    return response.data

async def unmatch_transaction_from_statement_line_db(match: ReconciliationMatchBase):
    response = (
        supabase.table("bank_statement_lines")
        .update({
            "is_matched": False,
            "treasury_transaction_id": None,
        })
        .eq("id", match.bank_statement_line_id)
        .execute()
    )
    return response.data


# Cash Balance Snapshot DB Operations

async def get_cash_balance_snapshots_db():
    response = supabase.table("cash_balance_snapshots").select("*").execute()
    return response.data

async def get_cash_balance_snapshots_by_account_db(account_id: int):
    response = supabase.table("cash_balance_snapshots").select("*").eq("account_id", account_id).execute()
    return response.data

async def get_cash_balance_snapshots_by_company_db(company_id: int):
    response = supabase.table("cash_balance_snapshots").select("*").eq("company_id", company_id).execute()
    return response.data

async def add_cash_balance_snapshot_db(snapshot: CashBalanceSnapshotBase):
    snapshot_data = _serialize(snapshot)
    response = supabase.table("cash_balance_snapshots").insert(snapshot_data).execute()
    return response.data


# Treasury Summary DB Operations

async def get_cash_summary_by_company_db():
    response = supabase.table("accounts").select("company_id, current_balance, currency").execute()
    summary = defaultdict(lambda: defaultdict(float))
    for account in response.data:
        company_id = account.get("company_id")
        currency = account.get("currency") or "UNKNOWN"
        summary[company_id][currency] += _to_float(account.get("current_balance"))
    return [
        {"company_id": company_id, "currency": currency, "total_balance": balance}
        for company_id, currencies in summary.items()
        for currency, balance in currencies.items()
    ]

async def get_cash_summary_by_currency_db():
    response = supabase.table("accounts").select("current_balance, currency").execute()
    summary = defaultdict(float)
    for account in response.data:
        currency = account.get("currency") or "UNKNOWN"
        summary[currency] += _to_float(account.get("current_balance"))
    return [
        {"currency": currency, "total_balance": balance}
        for currency, balance in summary.items()
    ]

async def get_upcoming_payables_db():
    today = date.today().isoformat()
    response = (
        supabase.table("payables")
        .select("*")
        .gte("due_date", today)
        .not_.in_("status", [PayableStatus.PAID.value, PayableStatus.CANCELLED.value])
        .order("due_date")
        .execute()
    )
    return response.data

async def get_upcoming_receivables_db():
    today = date.today().isoformat()
    response = (
        supabase.table("receivables")
        .select("*")
        .gte("due_date", today)
        .not_.in_("status", [ReceivableStatus.RECEIVED.value, ReceivableStatus.CANCELLED.value])
        .order("due_date")
        .execute()
    )
    return response.data

async def get_projected_cashflow_db():
    payables = await get_upcoming_payables_db()
    receivables = await get_upcoming_receivables_db()
    return {
        "upcoming_payables": payables,
        "upcoming_receivables": receivables,
        "net_projected": sum(_to_float(r.get("remaining_amount") or r.get("amount")) for r in receivables)
        - sum(_to_float(p.get("remaining_amount") or p.get("amount")) for p in payables),
    }

async def get_trade_cashflow_summary_db(trade_id: int):
    payables = await get_payables_by_trade_db(trade_id)
    receivables = await get_receivables_by_trade_db(trade_id)
    transactions = await get_transactions_by_trade_db(trade_id)
    return {
        "trade_id": trade_id,
        "payables": payables,
        "receivables": receivables,
        "transactions": transactions,
        "total_payables": sum(_to_float(p.get("amount")) for p in payables),
        "total_receivables": sum(_to_float(r.get("amount")) for r in receivables),
        "total_inflows": sum(
            _to_float(t.get("amount"))
            for t in transactions
            if t.get("transaction_type") == TransactionType.INFLOW.value
        ),
        "total_outflows": sum(
            _to_float(t.get("amount"))
            for t in transactions
            if t.get("transaction_type") == TransactionType.OUTFLOW.value
        ),
    }
