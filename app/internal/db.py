# app/internal/db.py

from app.connection import supabase
from app.internal.schemas import (
    CompanyBase,
    AccountBase,
    UserBase,
    ExpenseBase,
    ReimbursementBase,
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
    response = supabase.table("bank_accounts").select("*").execute()
    return response.data

async def get_account_db(account_id: int):
    response = supabase.table("bank_accounts").select("*").eq("id", account_id).execute()
    return response.data

async def add_account_db(account: AccountBase):
    account_data = account.model_dump(mode="json")
    response = supabase.table("bank_accounts").insert(account_data).execute()
    return response.data

async def update_account_db(account: AccountBase, account_id: int):
    account_data = account.model_dump(mode="json", exclude_unset=True)
    response = supabase.table("bank_accounts").update(account_data).eq("id", account_id).execute()
    return response.data

async def delete_account_db(account_id: int):
    response = supabase.table("bank_accounts").delete().eq("id", account_id).execute()
    return response.data

async def delete_accounts_db():
    response = supabase.table("bank_accounts").delete().neq("id", 0).execute()
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

async def add_expense_db(expense: ExpenseBase):
    expense_data = expense.model_dump(mode="json")
    response = supabase.table("expenses").insert(expense_data).execute()
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

async def delete_reimbursement_db(reimbursement_id: int):
    response = supabase.table("reimbursements").delete().eq("id", reimbursement_id).execute()
    return response.data

async def delete_reimbursements_db():
    response = supabase.table("reimbursements").delete().neq("id", 0).execute()
    return response.data
