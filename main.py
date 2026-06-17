from typing import Union
from fastapi import FastAPI
from dotenv import load_dotenv
from supabase import create_client, Client
from app.router import router
from app.activity_logs.router import router as activity_logs_router
from app.internal.router import router as internal_router
from app.auth.router import router as auth_router
from app.treasury.router import router as treasury_router
from app.financing.router import router as financing_router
from app.counterparties.router import router as counterparties_router
from app.trades.router import router as trades_router
from app.logistics.router import router as logistics_router

load_dotenv()

app = FastAPI()

app.include_router(activity_logs_router)
app.include_router(internal_router)
app.include_router(auth_router)
app.include_router(treasury_router)
app.include_router(financing_router)
app.include_router(counterparties_router)
app.include_router(trades_router)
app.include_router(logistics_router)
app.include_router(router)

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}