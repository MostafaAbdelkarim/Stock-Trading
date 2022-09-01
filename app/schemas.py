from datetime import datetime
from typing import List
from pydantic import BaseModel, EmailStr

from app.database import Base


class StockBase(BaseModel):
    name: str
    price: int
    availability: int


class StockResponse(StockBase):
    pass


class StockRequest(BaseModel):
    stock_id: str


class UserBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str
    amount: int


class UserOut(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr


class UserIn(BaseModel):
    user_id: str


class UserTransaction(BaseModel):
    user_id: str
    amount: int


class UserStockTransactions(BaseModel):
    user_id: str
    stock_id: str
    total: int
    upper_bound: int
    lower_bound: int


class UserResponse(BaseModel):
    name: str
    amount: int

    class Config():
        orm_mode = True
        allow_population_by_field_name = True


class UserStocksResponse(BaseModel):
    stocks: List[StockResponse]

    class Config():
        orm_mode = True
        allow_population_by_field_name = True


class StockOut(BaseModel):
    users: List[UserOut]

    class Config():
        orm_mode = True
        allow_population_by_field_name = True


class StockPriceOut(BaseModel):
    price: int

    class Config:
        orm_mode = True


class UserStockBase(BaseModel):
    user_id: str
    stock_id: str
    quantity: int
