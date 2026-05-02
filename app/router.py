# app/router.py

from fastapi import APIRouter
from app.managers import get_trades, create_trade

router = APIRouter()


@router.get("/trades")
def list_trades():
    return get_trades()


@router.post("/trades")
def add_trade(trade: dict):
    return create_trade(trade)