# app/financing/router.py

from fastapi import APIRouter
# from app.financing.managers import (
    
# )
# from app.financing.schemas import (
    
# )
from pydantic import BaseModel
from typing import List
from uuid import UUID

router = APIRouter(prefix="/financing", tags=["Financing"])

# TODO: Implement Financing Router

@router.get("/")
def read_root():
    return {"Hello": "World"}