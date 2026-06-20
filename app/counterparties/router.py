# app/counterparties/router.py

from fastapi import APIRouter
from app.counterparties.managers import (
    CounterpartyManager, 
    SPAManager
)
from app.counterparties.schemas import (
    CounterpartyBase, 
    SPABase
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

@router.post("/{counterparty_id}/contacts")
async def add_counterparty_contact(
    counterparty_id: int,
    contact: CounterpartyContactCreate,
):
    pass


@router.get("/{counterparty_id}/contacts")
async def get_counterparty_contacts(counterparty_id: int):
    pass


@router.get("/contacts/{contact_id}")
async def get_counterparty_contact(contact_id: int):
    pass


@router.patch("/contacts/{contact_id}")
async def update_counterparty_contact(
    contact_id: int,
    contact: CounterpartyContactUpdate,
):
    pass


@router.delete("/contacts/{contact_id}")
async def delete_counterparty_contact(contact_id: int):
    pass


# -------------------------
# Counterparty Bank Accounts
# -------------------------

@router.post("/{counterparty_id}/bank-accounts")
async def add_counterparty_bank_account(
    counterparty_id: int,
    bank_account: CounterpartyBankAccountCreate,
):
    pass


@router.get("/{counterparty_id}/bank-accounts")
async def get_counterparty_bank_accounts(counterparty_id: int):
    pass


@router.get("/bank-accounts/{bank_account_id}")
async def get_counterparty_bank_account(bank_account_id: int):
    pass


@router.patch("/bank-accounts/{bank_account_id}")
async def update_counterparty_bank_account(
    bank_account_id: int,
    bank_account: CounterpartyBankAccountUpdate,
):
    pass


@router.delete("/bank-accounts/{bank_account_id}")
async def delete_counterparty_bank_account(bank_account_id: int):
    pass


# -------------------------
# Counterparty KYC
# -------------------------

@router.post("/{counterparty_id}/kyc")
async def add_counterparty_kyc(
    counterparty_id: int,
    kyc: CounterpartyKYCCreate,
):
    pass


@router.get("/{counterparty_id}/kyc")
async def get_counterparty_kyc(counterparty_id: int):
    pass


@router.patch("/kyc/{kyc_id}")
async def update_counterparty_kyc(
    kyc_id: int,
    kyc: CounterpartyKYCUpdate,
):
    pass


@router.delete("/kyc/{kyc_id}")
async def delete_counterparty_kyc(kyc_id: int):
    pass


# -------------------------
# Counterparty SPAs
# -------------------------

@router.post("/{counterparty_id}/spas")
async def add_counterparty_spa(
    counterparty_id: int,
    spa: CounterpartySPACreate,
):
    pass


@router.get("/{counterparty_id}/spas")
async def get_counterparty_spas(counterparty_id: int):
    pass


@router.get("/spas/{spa_id}")
async def get_counterparty_spa(spa_id: int):
    pass


@router.patch("/spas/{spa_id}")
async def update_counterparty_spa(
    spa_id: int,
    spa: CounterpartySPAUpdate,
):
    pass


@router.delete("/spas/{spa_id}")
async def delete_counterparty_spa(spa_id: int):
    pass


@router.get("/spas/status/{status}")
async def get_spas_by_status(status: str):
    pass


@router.get("/spas/direction/{direction}")
async def get_spas_by_direction(direction: str):
    pass


@router.get("/company/{company_id}/spas")
async def get_spas_by_company(company_id: int):
    pass


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

# Counterparty Routers

@router.get("/counterparties")
async def get_counterparties():
    try:
        manager = CounterpartyManager(None)
        return await manager.get_counterparties()
    except Exception as e:
        raise e

@router.get("/counterparties/{counterparty_id}")
async def get_counterparty(counterparty_id: int):
    try:
        manager = CounterpartyManager(None)
        return await manager.get_counterparty(counterparty_id)
    except Exception as e:
        raise e

@router.post("/add_counterparty")
async def add_counterparty(counterparty: CounterpartyBase):
    try:
        manager = CounterpartyManager(counterparty)
        return await manager.add_counterparty()
    except Exception as e:
        raise e

@router.put("/update_counterparty/{counterparty_id}")
async def update_counterparty(counterparty_id: int, counterparty: CounterpartyBase):
    try:
        manager = CounterpartyManager(counterparty)
        return await manager.update_counterparty(counterparty_id)
    except Exception as e:
        raise e

@router.delete("/delete_counterparty/{counterparty_id}")
async def delete_counterparty(counterparty_id: int):
    try:
        manager = CounterpartyManager(None)
        return await manager.delete_counterparty(counterparty_id)
    except Exception as e:
        raise e

@router.delete("/delete_counterparties")
async def delete_counterparties():
    try:
        manager = CounterpartyManager(None)
        return await manager.delete_counterparties()
    except Exception as e:
        raise e

# SPA Routers

@router.get("/spas")
async def get_spas():
    try:
        manager = SPAManager(None)
        return await manager.get_spas()
    except Exception as e:
        raise e

@router.get("/spas/{spa_id}")
async def get_spa(spa_id: int):
    try:
        manager = SPAManager(None)
        return await manager.get_spa(spa_id)
    except Exception as e:
        raise e

@router.post("/add_spa")
async def add_spa(spa: SPABase):
    try:
        manager = SPAManager(spa)
        return await manager.add_spa()
    except Exception as e:
        raise e

@router.put("/update_spa/{spa_id}")
async def update_spa(spa_id: int, spa: SPABase):
    try:
        manager = SPAManager(spa)
        return await manager.update_spa(spa_id)
    except Exception as e:
        raise e

@router.delete("/delete_spa/{spa_id}")
async def delete_spa(spa_id: int):
    try:
        manager = SPAManager(None)
        return await manager.delete_spa(spa_id)
    except Exception as e:
        raise e

@router.delete("/delete_spas")
async def delete_spas():
    try:
        manager = SPAManager(None)
        return await manager.delete_spas()
    except Exception as e:
        raise e
