from typing import Optional
from pydantic import BaseModel, Field


class ArticleBase(BaseModel):
    name: str = Field(..., title="Article Name", max_length=100)
    description: str = Field(..., title="Article Description", max_length=200)
    unit_price: float = Field(..., title="Unit Price", ge=0)
    stock: int = Field(..., title="Stock", ge=0)
    sale_price: float = Field(..., title="Sale Price", ge=0)


class ArticleCreate(ArticleBase):
    id_Category: int = Field(..., title="Category ID", ge=1)
    id_Supplier: int = Field(..., title="Supplier ID", ge=1)


class ArticleUpdate(BaseModel):
    name: Optional[str] = Field(None, title="Article Name", max_length=100)
    description: Optional[str] = Field(None, title="Article Description", max_length=200)
    unit_price: Optional[float] = Field(None, title="Unit Price", ge=0)
    stock: Optional[int] = Field(None, title="Stock", ge=0)
    sale_price: Optional[float] = Field(None, title="Sale Price", ge=0)
    id_Category: Optional[int] = Field(None, title="Category ID", ge=1)
    id_Supplier: Optional[int] = Field(None, title="Supplier ID", ge=1)


class ArticleResponse(ArticleBase):
    id: int = Field(..., title="Article ID", ge=1)
    id_Category: int = Field(..., title="Category ID", ge=1)
    id_Supplier: int = Field(..., title="Supplier ID", ge=1)

    class Config:
        from_attributes = True