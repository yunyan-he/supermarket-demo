from pydantic import BaseModel
from typing import List, Optional
from datetime import date

class Item(BaseModel):
    barcode: str
    quantity: int

class CheckoutRequest(BaseModel):
    participant_external_id: str
    items: List[Item]

class ProductResponse(BaseModel):
    id: int
    name: str
    barcode: str
    price: float
    stock_quantity: int
    expiry_date: date

    class Config:
        orm_mode = True

class TransactionResponse(BaseModel):
    transaction_id: int
    total_amount: float
    status: str = "success"
