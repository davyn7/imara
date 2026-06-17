# app/treasury/router.py

from fastapi import APIRouter, Query
from app.treasury.managers import AccountManager, ExpenseManager, ReimbursementManager
from app.treasury.schemas import AccountBase, ExpenseBase, ReimbursementBase

router = APIRouter(prefix="/treasury", tags=["Treasury"])

# Account Routers

@router.get("/accounts")
async def get_accounts():
    try:
        manager = AccountManager(None)
        return await manager.get_accounts()
    except Exception as e:
        raise e

@router.get("/accounts/{account_id}")
async def get_account(account_id: int):
    try:
        manager = AccountManager(None)
        return await manager.get_account(account_id)
    except Exception as e:
        raise e

@router.post("/add_account")
async def add_account(account: AccountBase):
    try:
        manager = AccountManager(account)
        return await manager.add_account()
    except Exception as e:
        raise e

@router.put("/update_account/{account_id}")
async def update_account(account_id: int, account: AccountBase):
    try:
        manager = AccountManager(account)
        return await manager.update_account(account_id)
    except Exception as e:
        raise e

@router.delete("/delete_account/{account_id}")
async def delete_account(account_id: int):
    try:
        manager = AccountManager(None)
        return await manager.delete_account(account_id)
    except Exception as e:
        raise e

@router.delete("/delete_accounts")
async def delete_accounts():
    try:
        manager = AccountManager(None)
        return await manager.delete_accounts()
    except Exception as e:
        raise e

@router.get("/accounts/{account_id}/expenses/by_month")
async def get_account_expenses_by_month(
    account_id: int,
    month: int = Query(..., ge=1, le=12),
    year: int = Query(..., ge=2000, le=2100),
):
    try:
        manager = AccountManager(None)
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
        manager = AccountManager(None)
        return await manager.get_expense_total_by_month_year(account_id, month, year)
    except Exception as e:
        raise e

@router.get("/accounts/{account_id}/expenses/monthly_totals")
async def get_account_monthly_expense_totals(account_id: int):
    try:
        manager = AccountManager(None)
        return await manager.get_monthly_expense_totals(account_id)
    except Exception as e:
        raise e

# User Expense Routers

@router.get("/users/{user_id}/expenses/by_month")
async def get_user_expenses_by_month(
    user_id: int,
    month: int = Query(..., ge=1, le=12),
    year: int = Query(..., ge=2000, le=2100),
):
    try:
        manager = ExpenseManager(None)
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
        manager = ExpenseManager(None)
        return await manager.get_expense_total_by_user_month_year(user_id, month, year)
    except Exception as e:
        raise e

@router.get("/users/{user_id}/expenses/monthly_totals")
async def get_user_monthly_expense_totals(user_id: int):
    try:
        manager = ExpenseManager(None)
        return await manager.get_monthly_expense_totals_by_user(user_id)
    except Exception as e:
        raise e

# Expense Routers

@router.get("/expenses")
async def get_expenses():
    try:
        manager = ExpenseManager(None)
        return await manager.get_expenses()
    except Exception as e:
        raise e

@router.get("/expenses/by_month")
async def get_expenses_by_month(
    month: int = Query(..., ge=1, le=12),
    year: int = Query(..., ge=2000, le=2100),
):
    try:
        manager = ExpenseManager(None)
        return await manager.get_expenses_by_month_year(month, year)
    except Exception as e:
        raise e

@router.get("/expenses/total_by_month")
async def get_expense_total_by_month(
    month: int = Query(..., ge=1, le=12),
    year: int = Query(..., ge=2000, le=2100),
):
    try:
        manager = ExpenseManager(None)
        return await manager.get_expense_total_by_month_year(month, year)
    except Exception as e:
        raise e

@router.get("/expenses/monthly_totals")
async def get_monthly_expense_totals():
    try:
        manager = ExpenseManager(None)
        return await manager.get_monthly_expense_totals()
    except Exception as e:
        raise e

@router.get("/expenses/{expense_id}")
async def get_expense(expense_id: int):
    try:
        manager = ExpenseManager(None)
        return await manager.get_expense(expense_id)
    except Exception as e:
        raise e

@router.post("/add_expense")
async def add_expense(expense: ExpenseBase):
    try:
        manager = ExpenseManager(expense)
        return await manager.add_expense()
    except Exception as e:
        raise e

@router.put("/update_expense/{expense_id}")
async def update_expense(expense_id: int, expense: ExpenseBase):
    try:
        manager = ExpenseManager(expense)
        return await manager.update_expense(expense_id)
    except Exception as e:
        raise e

@router.delete("/delete_expense/{expense_id}")
async def delete_expense(expense_id: int):
    try:
        manager = ExpenseManager(None)
        return await manager.delete_expense(expense_id)
    except Exception as e:
        raise e

@router.delete("/delete_expenses")
async def delete_expenses():
    try:
        manager = ExpenseManager(None)
        return await manager.delete_expenses()
    except Exception as e:
        raise e

# Reimbursement Routers

@router.get("/reimbursements")
async def get_reimbursements():
    try:
        manager = ReimbursementManager(None)
        return await manager.get_reimbursements()
    except Exception as e:
        raise e

@router.get("/reimbursements/{reimbursement_id}")
async def get_reimbursement(reimbursement_id: int):
    try:
        manager = ReimbursementManager(None)
        return await manager.get_reimbursement(reimbursement_id)
    except Exception as e:
        raise e

@router.post("/add_reimbursement")
async def add_reimbursement(reimbursement: ReimbursementBase):
    try:
        manager = ReimbursementManager(reimbursement)
        return await manager.add_reimbursement()
    except Exception as e:
        raise e

@router.put("/update_reimbursement/{reimbursement_id}")
async def update_reimbursement(reimbursement_id: int, reimbursement: ReimbursementBase):
    try:
        manager = ReimbursementManager(reimbursement)
        return await manager.update_reimbursement(reimbursement_id)
    except Exception as e:
        raise e

@router.put("/mark_reimbursed/{reimbursement_id}")
async def mark_reimbursement_reimbursed(reimbursement_id: int):
    try:
        manager = ReimbursementManager(None)
        return await manager.mark_reimbursement_reimbursed(reimbursement_id)
    except Exception as e:
        raise e

@router.delete("/delete_reimbursement/{reimbursement_id}")
async def delete_reimbursement(reimbursement_id: int):
    try:
        manager = ReimbursementManager(None)
        return await manager.delete_reimbursement(reimbursement_id)
    except Exception as e:
        raise e

@router.delete("/delete_reimbursements")
async def delete_reimbursements():
    try:
        manager = ReimbursementManager(None)
        return await manager.delete_reimbursements()
    except Exception as e:
        raise e
