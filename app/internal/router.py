# app/internal/router.py

from fastapi import APIRouter
from app.internal.managers import (
    CompanyManager,
    AccountManager,
    UserManager,
    ExpenseManager,
    ReimbursementManager,
)
from app.internal.schemas import (
    CompanyBase,
    AccountBase,
    UserBase,
    ExpenseBase,
    ReimbursementBase,
)
router = APIRouter(prefix="/internal", tags=["Internal"])

# Company Routers

@router.get("/companies")
async def get_companies():
    try:
        manager = CompanyManager(None)
        return await manager.get_companies()
    except Exception as e:
        raise e

@router.get("/companies/{company_id}")
async def get_company(company_id: int):
    try:
        manager = CompanyManager(None)
        return await manager.get_company(company_id)
    except Exception as e:
        raise e

@router.post("/add_company")
async def add_company(company: CompanyBase):
    try:
        manager = CompanyManager(company)
        return await manager.add_company()
    except Exception as e:
        raise e

@router.put("/update_company/{company_id}")
async def update_company(company_id: int, company: CompanyBase):
    try:
        manager = CompanyManager(company)
        return await manager.update_company(company_id)
    except Exception as e:
        raise e

@router.delete("/delete_company/{company_id}")
async def delete_company(company_id: int):
    try:
        manager = CompanyManager(None)
        return await manager.delete_company(company_id)
    except Exception as e:
        raise e

@router.delete("/delete_companies")
async def delete_companies():
    try:
        manager = CompanyManager(None)
        return await manager.delete_companies()
    except Exception as e:
        raise e

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

# User Routers

@router.get("/users")
async def get_users():
    try:
        manager = UserManager(None)
        return await manager.get_users()
    except Exception as e:
        raise e

@router.get("/users/{user_id}")
async def get_user(user_id: int):
    try:
        manager = UserManager(None)
        return await manager.get_user(user_id)
    except Exception as e:
        raise e

@router.post("/add_user")
async def add_user(user: UserBase):
    try:
        manager = UserManager(user)
        return await manager.add_user()
    except Exception as e:
        raise e

@router.put("/update_user/{user_id}")
async def update_user(user_id: int, user: UserBase):
    try:
        manager = UserManager(user)
        return await manager.update_user(user_id)
    except Exception as e:
        raise e

@router.delete("/delete_user/{user_id}")
async def delete_user(user_id: int):
    try:
        manager = UserManager(None)
        return await manager.delete_user(user_id)
    except Exception as e:
        raise e

@router.delete("/delete_users")
async def delete_users():
    try:
        manager = UserManager(None)
        return await manager.delete_users()
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
