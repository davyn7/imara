# app/counterparties/managers.py

from app.counterparties.schemas import (
    CounterpartyCreate,
    CounterpartyUpdate,
    CounterpartyBase,
    SPABase,
)
from app.counterparties.db import (
    get_counterparties_db,
    get_counterparty_db,
    get_counterparties_by_company_db,
    get_counterparties_by_role_db,
    get_counterparties_by_status_db,
    add_counterparty_db,
    update_counterparty_db,
    delete_counterparty_db,
    delete_counterparties_db,
    get_spas_db,
    get_spa_db,
    add_spa_db,
    update_spa_db,
    delete_spa_db,
    delete_spas_db,
)

# Counterparty Manager

class CounterpartyManager:
    def __init__(self, counterparty: CounterpartyCreate | CounterpartyUpdate | CounterpartyBase | None = None):
        self.counterparty = counterparty

    async def get_counterparties(self):
        return await get_counterparties_db()

    async def get_counterparty(self, counterparty_id: int):
        return await get_counterparty_db(counterparty_id)

    async def get_counterparties_by_company(self, company_id: int):
        return await get_counterparties_by_company_db(company_id)

    async def get_counterparties_by_role(self, role: str):
        return await get_counterparties_by_role_db(role)

    async def get_counterparties_by_status(self, status: str):
        return await get_counterparties_by_status_db(status)

    async def add_counterparty(self):
        return await add_counterparty_db(self.counterparty)

    async def update_counterparty(self, counterparty_id: int):
        return await update_counterparty_db(self.counterparty, counterparty_id)

    async def delete_counterparty(self, counterparty_id: int):
        return await delete_counterparty_db(counterparty_id)

    async def delete_counterparties(self):
        return await delete_counterparties_db()

# SPA Manager

class SPAManager:
    def __init__(self, spa: SPABase):
        self.spa = spa

    async def get_spas(self):
        return await get_spas_db()

    async def get_spa(self, spa_id: int):
        return await get_spa_db(spa_id)

    async def add_spa(self):
        return await add_spa_db(self.spa)

    async def update_spa(self, spa_id: int):
        return await update_spa_db(self.spa, spa_id)

    async def delete_spa(self, spa_id: int):
        return await delete_spa_db(spa_id)

    async def delete_spas(self):
        return await delete_spas_db()
