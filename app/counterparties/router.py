# app/counterparties/router.py

from fastapi import APIRouter
from app.counterparties.managers import (
    CounterpartyManager,
    CounterpartyContactManager,
    CounterpartyBankAccountManager,
    CounterpartyKYCManager,
    CounterpartySPAManager,
)

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

router = APIRouter(prefix="/counterparties", tags=["Counterparties"])

# -------------------------
# Counterparties
# -------------------------

@router.post("/")
async def add_counterparty(counterparty: CounterpartyCreate):
    try:
        manager = CounterpartyManager(counterparty)
        return await manager.add_counterparty()
    except Exception as e:
        raise e


@router.get("/")
async def get_counterparties():
    try:
        manager = CounterpartyManager()
        return await manager.get_counterparties()
    except Exception as e:
        raise e


@router.get("/company/{company_id}")
async def get_counterparties_by_company(company_id: int):
    try:
        manager = CounterpartyManager()
        return await manager.get_counterparties_by_company(company_id)
    except Exception as e:
        raise e


@router.get("/role/{role}")
async def get_counterparties_by_role(role: str):
    try:
        manager = CounterpartyManager()
        return await manager.get_counterparties_by_role(role)
    except Exception as e:
        raise e


@router.get("/status/{status}")
async def get_counterparties_by_status(status: str):
    try:
        manager = CounterpartyManager()
        return await manager.get_counterparties_by_status(status)
    except Exception as e:
        raise e


@router.get("/{counterparty_id}")
async def get_counterparty(counterparty_id: int):
    try:
        manager = CounterpartyManager()
        return await manager.get_counterparty(counterparty_id)
    except Exception as e:
        raise e


@router.patch("/{counterparty_id}")
async def update_counterparty(counterparty_id: int, counterparty: CounterpartyUpdate):
    try:
        manager = CounterpartyManager(counterparty)
        return await manager.update_counterparty(counterparty_id)
    except Exception as e:
        raise e


@router.delete("/{counterparty_id}")
async def delete_counterparty(counterparty_id: int):
    try:
        manager = CounterpartyManager()
        return await manager.delete_counterparty(counterparty_id)
    except Exception as e:
        raise e


# -------------------------
# Counterparty Contacts
# -------------------------

@router.get("/contacts/{contact_id}")
async def get_counterparty_contact(contact_id: int):
    try:
        manager = CounterpartyContactManager()
        return await manager.get_counterparty_contact(contact_id)
    except Exception as e:
        raise e


@router.patch("/contacts/{contact_id}")
async def update_counterparty_contact(
    contact_id: int,
    contact: CounterpartyContactUpdate,
):
    try:
        manager = CounterpartyContactManager(contact)
        return await manager.update_counterparty_contact(contact_id)
    except Exception as e:
        raise e


@router.delete("/contacts/{contact_id}")
async def delete_counterparty_contact(contact_id: int):
    try:
        manager = CounterpartyContactManager()
        return await manager.delete_counterparty_contact(contact_id)
    except Exception as e:
        raise e


@router.post("/{counterparty_id}/contacts")
async def add_counterparty_contact(
    counterparty_id: int,
    contact: CounterpartyContactCreate,
):
    try:
        manager = CounterpartyContactManager(contact)
        return await manager.add_counterparty_contact(counterparty_id)
    except Exception as e:
        raise e


@router.get("/{counterparty_id}/contacts")
async def get_counterparty_contacts(counterparty_id: int):
    try:
        manager = CounterpartyContactManager()
        return await manager.get_counterparty_contacts(counterparty_id)
    except Exception as e:
        raise e


# -------------------------
# Counterparty Bank Accounts
# -------------------------

@router.get("/bank-accounts/{bank_account_id}")
async def get_counterparty_bank_account(bank_account_id: int):
    try:
        manager = CounterpartyBankAccountManager()
        return await manager.get_counterparty_bank_account(bank_account_id)
    except Exception as e:
        raise e


@router.patch("/bank-accounts/{bank_account_id}")
async def update_counterparty_bank_account(
    bank_account_id: int,
    bank_account: CounterpartyBankAccountUpdate,
):
    try:
        manager = CounterpartyBankAccountManager(bank_account)
        return await manager.update_counterparty_bank_account(bank_account_id)
    except Exception as e:
        raise e


@router.delete("/bank-accounts/{bank_account_id}")
async def delete_counterparty_bank_account(bank_account_id: int):
    try:
        manager = CounterpartyBankAccountManager()
        return await manager.delete_counterparty_bank_account(bank_account_id)
    except Exception as e:
        raise e


@router.post("/{counterparty_id}/bank-accounts")
async def add_counterparty_bank_account(
    counterparty_id: int,
    bank_account: CounterpartyBankAccountCreate,
):
    try:
        manager = CounterpartyBankAccountManager(bank_account)
        return await manager.add_counterparty_bank_account(counterparty_id)
    except Exception as e:
        raise e


@router.get("/{counterparty_id}/bank-accounts")
async def get_counterparty_bank_accounts(counterparty_id: int):
    try:
        manager = CounterpartyBankAccountManager()
        return await manager.get_counterparty_bank_accounts(counterparty_id)
    except Exception as e:
        raise e


# -------------------------
# Counterparty KYC
# -------------------------

@router.patch("/kyc/{kyc_id}")
async def update_counterparty_kyc(
    kyc_id: int,
    kyc: CounterpartyKYCUpdate,
):
    try:
        manager = CounterpartyKYCManager(kyc)
        return await manager.update_counterparty_kyc(kyc_id)
    except Exception as e:
        raise e


@router.delete("/kyc/{kyc_id}")
async def delete_counterparty_kyc(kyc_id: int):
    try:
        manager = CounterpartyKYCManager()
        return await manager.delete_counterparty_kyc(kyc_id)
    except Exception as e:
        raise e


@router.post("/{counterparty_id}/kyc")
async def add_counterparty_kyc(
    counterparty_id: int,
    kyc: CounterpartyKYCCreate,
):
    try:
        manager = CounterpartyKYCManager(kyc)
        return await manager.add_counterparty_kyc(counterparty_id)
    except Exception as e:
        raise e


@router.get("/{counterparty_id}/kyc")
async def get_counterparty_kyc(counterparty_id: int):
    try:
        manager = CounterpartyKYCManager()
        return await manager.get_counterparty_kyc(counterparty_id)
    except Exception as e:
        raise e


# -------------------------
# Counterparty SPAs
# -------------------------

@router.get("/spas/status/{status}")
async def get_spas_by_status(status: str):
    try:
        manager = CounterpartySPAManager()
        return await manager.get_spas_by_status(status)
    except Exception as e:
        raise e


@router.get("/spas/direction/{direction}")
async def get_spas_by_direction(direction: str):
    try:
        manager = CounterpartySPAManager()
        return await manager.get_spas_by_direction(direction)
    except Exception as e:
        raise e


@router.get("/company/{company_id}/spas")
async def get_spas_by_company(company_id: int):
    try:
        manager = CounterpartySPAManager()
        return await manager.get_spas_by_company(company_id)
    except Exception as e:
        raise e


@router.get("/spas/{spa_id}")
async def get_counterparty_spa(spa_id: int):
    try:
        manager = CounterpartySPAManager()
        return await manager.get_counterparty_spa(spa_id)
    except Exception as e:
        raise e


@router.patch("/spas/{spa_id}")
async def update_counterparty_spa(
    spa_id: int,
    spa: CounterpartySPAUpdate,
):
    try:
        manager = CounterpartySPAManager(spa)
        return await manager.update_counterparty_spa(spa_id)
    except Exception as e:
        raise e


@router.delete("/spas/{spa_id}")
async def delete_counterparty_spa(spa_id: int):
    try:
        manager = CounterpartySPAManager()
        return await manager.delete_counterparty_spa(spa_id)
    except Exception as e:
        raise e


@router.post("/{counterparty_id}/spas")
async def add_counterparty_spa(
    counterparty_id: int,
    spa: CounterpartySPACreate,
):
    try:
        manager = CounterpartySPAManager(spa)
        return await manager.add_counterparty_spa(counterparty_id)
    except Exception as e:
        raise e


@router.get("/{counterparty_id}/spas")
async def get_counterparty_spas(counterparty_id: int):
    try:
        manager = CounterpartySPAManager()
        return await manager.get_counterparty_spas(counterparty_id)
    except Exception as e:
        raise e


# -------------------------
# Counterparty Documents
# -------------------------

@router.post("/{counterparty_id}/documents")
async def add_counterparty_document(
    counterparty_id: int,
    document: CounterpartyDocumentCreate,
):
    pass


@router.get("/{counterparty_id}/documents")
async def get_counterparty_documents(counterparty_id: int):
    pass


@router.get("/documents/{document_id}")
async def get_counterparty_document(document_id: int):
    pass


@router.patch("/documents/{document_id}")
async def update_counterparty_document(
    document_id: int,
    document: CounterpartyDocumentUpdate,
):
    pass


@router.delete("/documents/{document_id}")
async def delete_counterparty_document(document_id: int):
    pass
