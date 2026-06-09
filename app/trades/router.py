# app/trades/router.py

from fastapi import APIRouter
# from app.trades.managers import (
    
# )
# from app.trades.schemas import (
    
# )
from pydantic import BaseModel
from typing import List
from uuid import UUID

router = APIRouter(prefix="/trades", tags=["Trades"])

# TODO: Implement Trades Router

@router.get("/")
def read_root():
    return {"Hello": "World"}