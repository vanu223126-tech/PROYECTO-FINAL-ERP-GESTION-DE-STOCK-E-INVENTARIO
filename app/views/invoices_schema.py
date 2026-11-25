from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class InvoiceDetailBase(BaseModel):
    id_article: int = Field(..., gt=0)
    amount: int = Field(..., gt=0)
    unit_price: float = Field(..., ge=0)


class InvoiceDetailCreate(InvoiceDetailBase):
    pass


class InvoiceDetailResponse(InvoiceDetailBase):
    id: int
    subtotal: float = Field(..., ge=0)

    class Config:
        from_attributes = True


class InvoiceBase(BaseModel):
    id_customer: int = Field(..., gt=0)
    id_branch: Optional[int] = None


class InvoiceCreate(InvoiceBase):
    date: str = Field(..., min_length=10, max_length=10)
    items: list[InvoiceDetailCreate] = Field(..., min_length=1)



class InvoiceUpdate(BaseModel):
    id_customer: Optional[int] = Field(None, gt=0)
    id_branch: Optional[int] = None
    items: Optional[list[InvoiceDetailCreate]] = None


class InvoiceResponse(InvoiceBase):
    id: int
    total: float = Field(..., ge=0)
    date: Optional[str | datetime] = None
    items: list[InvoiceDetailResponse] = Field(default_factory=list)


    class Config:
        from_attributes = True