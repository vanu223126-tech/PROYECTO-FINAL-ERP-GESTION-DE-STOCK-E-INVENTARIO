from typing import Optional
from pydantic import BaseModel, Field


class SupplierBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=150)
    contact_name: Optional[str] = Field(None, max_length=150)
    phone: Optional[str] = Field(None, max_length=50)
    email: Optional[str] = Field(None, max_length=150)
    address: Optional[str] = Field(None, max_length=200)


class SupplierCreate(SupplierBase):
    pass


class SupplierUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=150)
    contact_name: Optional[str] = Field(None, max_length=150)
    phone: Optional[str] = Field(None, max_length=50)
    email: Optional[str] = Field(None, max_length=150)
    address: Optional[str] = Field(None, max_length=200)


class SupplierResponse(SupplierBase):
    id: int

    class Config:
        from_attributes = True