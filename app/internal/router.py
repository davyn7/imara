# app/internal/router.py

from fastapi import APIRouter
# from app.internal.managers import (
    
# )
# from app.internal.schemas import (
    
# )
from pydantic import BaseModel
from typing import List
from uuid import UUID

router = APIRouter(prefix="/internal", tags=["Internal"])

# TODO: Implement Internal Router

@router.get("/")
def read_root():
    return {"Hello": "World"}