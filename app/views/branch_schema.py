from typing import Optional
from pydantic import BaseModel, Field


class BranchBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=150)
    address: str = Field(..., min_length=1, max_length=200)
    phone: str = Field(..., min_length=1, max_length=50)


class BranchCreate(BranchBase):
    pass


class BranchResponse(BranchBase):
    id: int

    class Config:
        from_attributes = True