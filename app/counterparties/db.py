# app/counterparties/db.py

from app.connection import supabase
from app.counterparties.schemas import (
    CounterpartyCreate,
    CounterpartyUpdate,
    CounterpartyContactCreate,
    CounterpartyContactUpdate,
    CounterpartyBankAccountCreate,
    CounterpartyBankAccountUpdate,
    CounterpartyKYCCreate,
    CounterpartyKYCUpdate,
    CounterpartySPACreate,
    CounterpartySPAUpdate,
    CounterpartyDocumentCreate,
    CounterpartyDocumentUpdate,
)


def _serialize(model) -> dict:
    return model.model_dump(mode="json")


# Counterparty DB Operations

async def get_counterparties_db():
    response = supabase.table("counterparties").select("*").execute()
    return response.data

async def get_counterparty_db(counterparty_id: int):
    response = supabase.table("counterparties").select("*").eq("id", counterparty_id).execute()
    return response.data

async def get_counterparties_by_company_db(company_id: int):
    response = (
        supabase.table("counterparties")
        .select("*")
        .eq("company_id", company_id)
        .execute()
    )
    return response.data

async def get_counterparties_by_role_db(role: str):
    response = (
        supabase.table("counterparties")
        .select("*")
        .contains("roles", [role])
        .execute()
    )
    return response.data

async def get_counterparties_by_status_db(status: str):
    response = (
        supabase.table("counterparties")
        .select("*")
        .eq("status", status)
        .execute()
    )
    return response.data

async def add_counterparty_db(counterparty: CounterpartyCreate):
    counterparty_data = _serialize(counterparty)
    response = supabase.table("counterparties").insert(counterparty_data).execute()
    return response.data

async def update_counterparty_db(counterparty: CounterpartyUpdate, counterparty_id: int):
    counterparty_data = counterparty.model_dump(mode="json", exclude_unset=True)
    response = (
        supabase.table("counterparties")
        .update(counterparty_data)
        .eq("id", counterparty_id)
        .execute()
    )
    return response.data

async def delete_counterparty_db(counterparty_id: int):
    response = supabase.table("counterparties").delete().eq("id", counterparty_id).execute()
    return response.data

# Counterparty Contact DB Operations

async def get_counterparty_contacts_db(counterparty_id: int):
    response = (
        supabase.table("counterparty_contacts")
        .select("*")
        .eq("counterparty_id", counterparty_id)
        .execute()
    )
    return response.data

async def get_counterparty_contact_db(contact_id: int):
    response = (
        supabase.table("counterparty_contacts")
        .select("*")
        .eq("id", contact_id)
        .execute()
    )
    return response.data

async def add_counterparty_contact_db(counterparty_id: int, contact: CounterpartyContactCreate):
    contact_data = _serialize(contact)
    contact_data["counterparty_id"] = counterparty_id
    response = supabase.table("counterparty_contacts").insert(contact_data).execute()
    return response.data

async def update_counterparty_contact_db(contact: CounterpartyContactUpdate, contact_id: int):
    contact_data = contact.model_dump(mode="json", exclude_unset=True)
    response = (
        supabase.table("counterparty_contacts")
        .update(contact_data)
        .eq("id", contact_id)
        .execute()
    )
    return response.data

async def delete_counterparty_contact_db(contact_id: int):
    response = (
        supabase.table("counterparty_contacts")
        .delete()
        .eq("id", contact_id)
        .execute()
    )
    return response.data

# Counterparty Bank Account DB Operations

async def get_counterparty_bank_accounts_db(counterparty_id: int):
    response = (
        supabase.table("counterparty_bank_accounts")
        .select("*")
        .eq("counterparty_id", counterparty_id)
        .execute()
    )
    return response.data

async def get_counterparty_bank_account_db(bank_account_id: int):
    response = (
        supabase.table("counterparty_bank_accounts")
        .select("*")
        .eq("id", bank_account_id)
        .execute()
    )
    return response.data

async def add_counterparty_bank_account_db(
    counterparty_id: int,
    bank_account: CounterpartyBankAccountCreate,
):
    bank_account_data = _serialize(bank_account)
    bank_account_data["counterparty_id"] = counterparty_id
    response = supabase.table("counterparty_bank_accounts").insert(bank_account_data).execute()
    return response.data

async def update_counterparty_bank_account_db(
    bank_account: CounterpartyBankAccountUpdate,
    bank_account_id: int,
):
    bank_account_data = bank_account.model_dump(mode="json", exclude_unset=True)
    response = (
        supabase.table("counterparty_bank_accounts")
        .update(bank_account_data)
        .eq("id", bank_account_id)
        .execute()
    )
    return response.data

async def delete_counterparty_bank_account_db(bank_account_id: int):
    response = (
        supabase.table("counterparty_bank_accounts")
        .delete()
        .eq("id", bank_account_id)
        .execute()
    )
    return response.data

# Counterparty KYC DB Operations

async def get_counterparty_kyc_db(counterparty_id: int):
    response = (
        supabase.table("counterparty_kyc")
        .select("*")
        .eq("counterparty_id", counterparty_id)
        .execute()
    )
    return response.data

async def add_counterparty_kyc_db(counterparty_id: int, kyc: CounterpartyKYCCreate):
    kyc_data = _serialize(kyc)
    kyc_data["counterparty_id"] = counterparty_id
    response = supabase.table("counterparty_kyc").insert(kyc_data).execute()
    return response.data

async def update_counterparty_kyc_db(kyc: CounterpartyKYCUpdate, kyc_id: int):
    kyc_data = kyc.model_dump(mode="json", exclude_unset=True)
    response = (
        supabase.table("counterparty_kyc")
        .update(kyc_data)
        .eq("id", kyc_id)
        .execute()
    )
    return response.data

async def delete_counterparty_kyc_db(kyc_id: int):
    response = (
        supabase.table("counterparty_kyc")
        .delete()
        .eq("id", kyc_id)
        .execute()
    )
    return response.data

# Counterparty SPA DB Operations

async def get_counterparty_spas_db(counterparty_id: int):
    response = (
        supabase.table("counterparty_spas")
        .select("*")
        .eq("counterparty_id", counterparty_id)
        .execute()
    )
    return response.data

async def get_counterparty_spa_db(spa_id: int):
    response = (
        supabase.table("counterparty_spas")
        .select("*")
        .eq("id", spa_id)
        .execute()
    )
    return response.data

async def get_spas_by_status_db(status: str):
    response = (
        supabase.table("counterparty_spas")
        .select("*")
        .eq("status", status)
        .execute()
    )
    return response.data

async def get_spas_by_direction_db(direction: str):
    response = (
        supabase.table("counterparty_spas")
        .select("*")
        .eq("direction", direction)
        .execute()
    )
    return response.data

async def get_spas_by_company_db(company_id: int):
    response = (
        supabase.table("counterparty_spas")
        .select("*")
        .eq("company_id", company_id)
        .execute()
    )
    return response.data

async def add_counterparty_spa_db(counterparty_id: int, spa: CounterpartySPACreate):
    spa_data = _serialize(spa)
    spa_data["counterparty_id"] = counterparty_id
    response = supabase.table("counterparty_spas").insert(spa_data).execute()
    return response.data

async def update_counterparty_spa_db(spa: CounterpartySPAUpdate, spa_id: int):
    spa_data = spa.model_dump(mode="json", exclude_unset=True)
    response = (
        supabase.table("counterparty_spas")
        .update(spa_data)
        .eq("id", spa_id)
        .execute()
    )
    return response.data

async def delete_counterparty_spa_db(spa_id: int):
    response = (
        supabase.table("counterparty_spas")
        .delete()
        .eq("id", spa_id)
        .execute()
    )
    return response.data

# Counterparty Document DB Operations

async def get_counterparty_documents_db(counterparty_id: int):
    response = (
        supabase.table("counterparty_documents")
        .select("*")
        .eq("counterparty_id", counterparty_id)
        .execute()
    )
    return response.data

async def get_counterparty_document_db(document_id: int):
    response = (
        supabase.table("counterparty_documents")
        .select("*")
        .eq("id", document_id)
        .execute()
    )
    return response.data

async def add_counterparty_document_db(
    counterparty_id: int,
    document: CounterpartyDocumentCreate,
):
    document_data = _serialize(document)
    document_data["counterparty_id"] = counterparty_id
    response = supabase.table("counterparty_documents").insert(document_data).execute()
    return response.data

async def update_counterparty_document_db(
    document: CounterpartyDocumentUpdate,
    document_id: int,
):
    document_data = document.model_dump(mode="json", exclude_unset=True)
    response = (
        supabase.table("counterparty_documents")
        .update(document_data)
        .eq("id", document_id)
        .execute()
    )
    return response.data

async def delete_counterparty_document_db(document_id: int):
    response = (
        supabase.table("counterparty_documents")
        .delete()
        .eq("id", document_id)
        .execute()
    )
    return response.data
