# app/counterparties/router.py

from fastapi import APIRouter
# from app.counterparties.managers import (
    
# )
# from app.counterparties.schemas import (
    
# )
from pydantic import BaseModel
from typing import List
from uuid import UUID

router = APIRouter(prefix="/counterparties", tags=["Counterparties"])

# TODO: Implement Counterparties Router

@router.get("/")
def read_root():
    return {"Hello": "World"}