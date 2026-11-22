from typing import Optional
from pydantic import BaseModel, Field


class DepositBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=150)
    id_branch: Optional[int] = None


class DepositCreate(DepositBase):
    pass


class DepositUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=150)
    id_branch: Optional[int] = None


class DepositResponse(DepositBase):
    id: int

    class Config:
        from_attributes = True