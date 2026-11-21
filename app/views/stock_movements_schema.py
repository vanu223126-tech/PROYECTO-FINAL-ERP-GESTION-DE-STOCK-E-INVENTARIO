from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class StockMovementBase(BaseModel):
    id_article: int = Field(..., gt=0)
    id_deposit: Optional[int] = None
    movement_type: str = Field(..., min_length=1, max_length=50)
    quantity: int = Field(..., gt=0)
    reason: Optional[str] = Field(None, max_length=255)


class StockMovementCreate(StockMovementBase):
    pass


class StockMovementResponse(StockMovementBase):
    id: int
    movement_date: Optional[str | datetime] = None

    class Config:
        from_attributes = True