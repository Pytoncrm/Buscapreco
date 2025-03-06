from pydantic import BaseModel
from typing import List, Optional

class SaleBase(BaseModel):
    product_name: str
    price: float

class SaleCreate(SaleBase):
    pass

class Sale(SaleBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True

class UserBase(BaseModel):
    name: str
    email: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    sales: List[Sale] = []

    class Config:
        from_attributes = True
