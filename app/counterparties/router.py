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

router = APIRouter(prefix="/counterparties", tags=["Counterparties"])

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
