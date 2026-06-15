# app/internal/db.py

import calendar
from collections import defaultdict
from datetime import date

from app.connection import supabase
from app.internal.schemas import (
    CompanyBase,
    AccountBase,
    UserBase,
    ExpenseBase,
    ReimbursementBase
)

# Company DB Operations

async def get_companies_db():
    response = supabase.table("companies").select("*").execute()
    return response.data

async def get_company_db(company_id: int):
    response = supabase.table("companies").select("*").eq("id", company_id).execute()
    return response.data

async def add_company_db(company: CompanyBase):
    company_data = company.model_dump()
    response = supabase.table("companies").insert(company_data).execute()
    return response.data

async def update_company_db(company: CompanyBase, company_id: int):
    company_data = company.model_dump(exclude_unset=True)
    response = supabase.table("companies").update(company_data).eq("id", company_id).execute()
    return response.data

async def delete_company_db(company_id: int):
    response = supabase.table("companies").delete().eq("id", company_id).execute()
    return response.data

async def delete_companies_db():
    response = supabase.table("companies").delete().neq("id", 0).execute()
    return response.data

# Account DB Operations

async def get_accounts_db():
    response = supabase.table("accounts").select("*").execute()
    return response.data

async def get_account_db(account_id: int):
    response = supabase.table("accounts").select("*").eq("id", account_id).execute()
    return response.data

async def add_account_db(account: AccountBase):
    account_data = account.model_dump(mode="json")
    response = supabase.table("accounts").insert(account_data).execute()
    return response.data

async def update_account_db(account: AccountBase, account_id: int):
    account_data = account.model_dump(mode="json", exclude_unset=True)
    response = supabase.table("accounts").update(account_data).eq("id", account_id).execute()
    return response.data

async def delete_account_db(account_id: int):
    response = supabase.table("accounts").delete().eq("id", account_id).execute()
    return response.data

async def delete_accounts_db():
    response = supabase.table("accounts").delete().neq("id", 0).execute()
    return response.data

async def deduct_account_balance_db(account_id: int, amount: float):
    response = supabase.table("accounts").select("current_balance").eq("id", account_id).execute()
    if not response.data:
        return None
    current_balance = response.data[0].get("current_balance") or 0
    new_balance = current_balance - amount
    response = supabase.table("accounts").update({"current_balance": new_balance}).eq("id", account_id).execute()
    return response.data

# User DB Operations

async def get_users_db():
    response = supabase.table("users").select("*").execute()
    return response.data

async def get_user_db(user_id: int):
    response = supabase.table("users").select("*").eq("id", user_id).execute()
    return response.data

async def add_user_db(user: UserBase):
    user_data = user.model_dump(mode="json")
    response = supabase.table("users").insert(user_data).execute()
    return response.data

async def update_user_db(user: UserBase, user_id: int):
    user_data = user.model_dump(mode="json", exclude_unset=True)
    response = supabase.table("users").update(user_data).eq("id", user_id).execute()
    return response.data

async def delete_user_db(user_id: int):
    response = supabase.table("users").delete().eq("id", user_id).execute()
    return response.data

async def delete_users_db():
    response = supabase.table("users").delete().neq("id", 0).execute()
    return response.data

# Expense DB Operations

async def get_expenses_db():
    response = supabase.table("expenses").select("*").execute()
    return response.data

async def get_expense_db(expense_id: int):
    response = supabase.table("expenses").select("*").eq("id", expense_id).execute()
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
    total = sum(expense["amount"] for expense in response.data if expense.get("amount") is not None)
    return {"year": year, "month": month, "total": total}

async def get_monthly_expense_totals_db():
    response = supabase.table("expenses").select("amount, expense_date").execute()
    totals = defaultdict(float)
    for expense in response.data:
        expense_date = expense.get("expense_date")
        amount = expense.get("amount")
        if not expense_date or amount is None:
            continue
        year = int(expense_date[:4])
        month = int(expense_date[5:7])
        totals[(year, month)] += amount
    return [
        {"year": year, "month": month, "total": total}
        for (year, month), total in sorted(totals.items(), reverse=True)
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
    total = sum(expense["amount"] for expense in response.data if expense.get("amount") is not None)
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
        year = int(expense_date[:4])
        month = int(expense_date[5:7])
        totals[(year, month)] += amount
    return [
        {"account_id": account_id, "year": year, "month": month, "total": total}
        for (year, month), total in sorted(totals.items(), reverse=True)
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
    total = sum(expense["amount"] for expense in response.data if expense.get("amount") is not None)
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
        year = int(expense_date[:4])
        month = int(expense_date[5:7])
        totals[(year, month)] += amount
    return [
        {"user_id": user_id, "year": year, "month": month, "total": total}
        for (year, month), total in sorted(totals.items(), reverse=True)
    ]

async def add_expense_db(expense: ExpenseBase):
    expense_data = expense.model_dump(mode="json")
    response = supabase.table("expenses").insert(expense_data).execute()
    if not expense.is_reimbursement and expense.account_id and expense.amount:
        await deduct_account_balance_db(expense.account_id, expense.amount)
    return response.data

async def update_expense_db(expense: ExpenseBase, expense_id: int):
    expense_data = expense.model_dump(mode="json", exclude_unset=True)
    response = supabase.table("expenses").update(expense_data).eq("id", expense_id).execute()
    return response.data

async def delete_expense_db(expense_id: int):
    response = supabase.table("expenses").delete().eq("id", expense_id).execute()
    return response.data

async def delete_expenses_db():
    response = supabase.table("expenses").delete().neq("id", 0).execute()
    return response.data

# Reimbursement DB Operations

async def get_reimbursements_db():
    response = supabase.table("reimbursements").select("*").execute()
    return response.data

async def get_reimbursement_db(reimbursement_id: int):
    response = supabase.table("reimbursements").select("*").eq("id", reimbursement_id).execute()
    return response.data

async def add_reimbursement_db(reimbursement: ReimbursementBase):
    reimbursement_data = reimbursement.model_dump(mode="json")
    response = supabase.table("reimbursements").insert(reimbursement_data).execute()
    return response.data

async def update_reimbursement_db(reimbursement: ReimbursementBase, reimbursement_id: int):
    reimbursement_data = reimbursement.model_dump(mode="json", exclude_unset=True)
    response = supabase.table("reimbursements").update(reimbursement_data).eq("id", reimbursement_id).execute()
    return response.data

async def mark_reimbursement_reimbursed_db(reimbursement_id: int):
    reimbursement_response = (
        supabase.table("reimbursements")
        .select("*")
        .eq("id", reimbursement_id)
        .execute()
    )
    if not reimbursement_response.data:
        return None
    reimbursement = reimbursement_response.data[0]
    if reimbursement.get("is_reimbursed"):
        return reimbursement_response.data
    expense_id = reimbursement.get("expense_id")
    if not expense_id:
        return None
    expense_response = (
        supabase.table("expenses")
        .select("account_id, amount")
        .eq("id", expense_id)
        .execute()
    )
    if not expense_response.data:
        return None
    expense = expense_response.data[0]
    account_id = expense.get("account_id")
    amount = expense.get("amount")
    if account_id and amount:
        await deduct_account_balance_db(account_id, amount)
    response = (
        supabase.table("reimbursements")
        .update({"is_reimbursed": True})
        .eq("id", reimbursement_id)
        .execute()
    )
    return response.data

async def delete_reimbursement_db(reimbursement_id: int):
    response = supabase.table("reimbursements").delete().eq("id", reimbursement_id).execute()
    return response.data

async def delete_reimbursements_db():
    response = supabase.table("reimbursements").delete().neq("id", 0).execute()
    return response.data
