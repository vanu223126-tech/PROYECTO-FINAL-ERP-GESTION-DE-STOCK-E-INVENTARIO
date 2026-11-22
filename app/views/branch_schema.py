from typing import Optional
from pydantic import BaseModel, Field


class BranchBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=150)
    address: str = Field(..., min_length=1, max_length=200)
    phone: str = Field(..., min_length=1, max_length=50)


class BranchCreate(BranchBase):
    pass


class BranchUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=150)
    address: Optional[str] = Field(None, min_length=1, max_length=200)
    phone: Optional[str] = Field(None, min_length=1, max_length=50)


class BranchResponse(BranchBase):
    id: int

    class Config:
        from_attributes = True