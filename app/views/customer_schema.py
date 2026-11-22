from typing import Optional
from pydantic import BaseModel, Field


class CustomerBase(BaseModel):
    name: str = Field(..., title="Customer Name", min_length=1, max_length=100)
    email: str = Field(..., title="Customer Email", min_length=1, max_length=100)
    phone: str = Field(..., title="Customer Phone", min_length=1, max_length=15)
    address: str = Field(..., title="Customer Address", min_length=1, max_length=200)
    registration_date: str = Field(
        ..., title="Customer Registration Date", min_length=10, max_length=10
    )


class CustomerCreate(CustomerBase):
    pass


class CustomerUpdate(BaseModel):
    name: Optional[str] = Field(None, title="Customer Name", min_length=1, max_length=100)
    email: Optional[str] = Field(None, title="Customer Email", min_length=1, max_length=100)
    phone: Optional[str] = Field(None, title="Customer Phone", min_length=1, max_length=15)
    address: Optional[str] = Field(None, title="Customer Address", min_length=1, max_length=200)
    registration_date: Optional[str] = Field(
        None, title="Customer Registration Date", min_length=10, max_length=10
    )


class CustomerResponse(CustomerBase):
    id: int = Field(..., title="Customer ID", ge=1)

    class Config:
        from_attributes = True