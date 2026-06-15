# app/internal/managers.py

from app.internal.schemas import (
    CompanyBase,
    AccountBase,
    UserBase,
    ExpenseBase,
    ReimbursementBase
)
from app.internal.db import (
    get_companies_db,
    get_company_db,
    add_company_db,
    update_company_db,
    delete_company_db,
    delete_companies_db,
    get_accounts_db,
    get_account_db,
    add_account_db,
    update_account_db,
    delete_account_db,
    delete_accounts_db,
    get_users_db,
    get_user_db,
    add_user_db,
    update_user_db,
    delete_user_db,
    delete_users_db,
    get_expenses_db,
    get_expense_db,
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
    delete_expenses_db,
    get_reimbursements_db,
    get_reimbursement_db,
    add_reimbursement_db,
    update_reimbursement_db,
    mark_reimbursement_reimbursed_db,
    delete_reimbursement_db,
    delete_reimbursements_db
)
# Company Manager

class CompanyManager:
    def __init__(self, company: CompanyBase):
        self.company = company

    async def get_companies(self):
        return await get_companies_db()

    async def get_company(self, company_id: int):
        return await get_company_db(company_id)

    async def add_company(self):
        return await add_company_db(self.company)

    async def update_company(self, company_id: int):
        return await update_company_db(self.company, company_id)

    async def delete_company(self, company_id: int):
        return await delete_company_db(company_id)

    async def delete_companies(self):
        return await delete_companies_db()

# Account Manager

class AccountManager:
    def __init__(self, account: AccountBase):
        self.account = account

    async def get_accounts(self):
        return await get_accounts_db()

    async def get_account(self, account_id: int):
        return await get_account_db(account_id)

    async def add_account(self):
        return await add_account_db(self.account)

    async def update_account(self, account_id: int):
        return await update_account_db(self.account, account_id)

    async def delete_account(self, account_id: int):
        return await delete_account_db(account_id)

    async def delete_accounts(self):
        return await delete_accounts_db()

    async def get_expenses_by_month_year(self, account_id: int, month: int, year: int):
        return await get_expenses_by_account_month_year_db(account_id, month, year)

    async def get_expense_total_by_month_year(self, account_id: int, month: int, year: int):
        return await get_expense_total_by_account_month_year_db(account_id, month, year)

    async def get_monthly_expense_totals(self, account_id: int):
        return await get_monthly_expense_totals_by_account_db(account_id)

# User Manager

class UserManager:
    def __init__(self, user: UserBase):
        self.user = user

    async def get_users(self):
        return await get_users_db()

    async def get_user(self, user_id: int):
        return await get_user_db(user_id)

    async def add_user(self):
        return await add_user_db(self.user)

    async def update_user(self, user_id: int):
        return await update_user_db(self.user, user_id)

    async def delete_user(self, user_id: int):
        return await delete_user_db(user_id)

    async def delete_users(self):
        return await delete_users_db()

    async def get_expenses_by_month_year(self, user_id: int, month: int, year: int):
        return await get_expenses_by_user_month_year_db(user_id, month, year)

    async def get_expense_total_by_month_year(self, user_id: int, month: int, year: int):
        return await get_expense_total_by_user_month_year_db(user_id, month, year)

    async def get_monthly_expense_totals(self, user_id: int):
        return await get_monthly_expense_totals_by_user_db(user_id)

# Expense Manager

class ExpenseManager:
    def __init__(self, expense: ExpenseBase):
        self.expense = expense

    async def get_expenses(self):
        return await get_expenses_db()

    async def get_expense(self, expense_id: int):
        return await get_expense_db(expense_id)

    async def get_expenses_by_month_year(self, month: int, year: int):
        return await get_expenses_by_month_year_db(month, year)

    async def get_expense_total_by_month_year(self, month: int, year: int):
        return await get_expense_total_by_month_year_db(month, year)

    async def get_monthly_expense_totals(self):
        return await get_monthly_expense_totals_db()

    async def add_expense(self):
        return await add_expense_db(self.expense)

    async def update_expense(self, expense_id: int):
        return await update_expense_db(self.expense, expense_id)

    async def delete_expense(self, expense_id: int):
        return await delete_expense_db(expense_id)

    async def delete_expenses(self):
        return await delete_expenses_db()

# Reimbursement Manager

class ReimbursementManager:
    def __init__(self, reimbursement: ReimbursementBase):
        self.reimbursement = reimbursement

    async def get_reimbursements(self):
        return await get_reimbursements_db()

    async def get_reimbursement(self, reimbursement_id: int):
        return await get_reimbursement_db(reimbursement_id)

    async def add_reimbursement(self):
        return await add_reimbursement_db(self.reimbursement)

    async def update_reimbursement(self, reimbursement_id: int):
        return await update_reimbursement_db(self.reimbursement, reimbursement_id)

    async def mark_reimbursement_reimbursed(self, reimbursement_id: int):
        return await mark_reimbursement_reimbursed_db(reimbursement_id)

    async def delete_reimbursement(self, reimbursement_id: int):
        return await delete_reimbursement_db(reimbursement_id)

    async def delete_reimbursements(self):
        return await delete_reimbursements_db()
