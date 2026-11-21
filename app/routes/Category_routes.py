import sqlite3
from typing import List
from fastapi import APIRouter, Depends, status

from app.controllers.Category_controller import CategoryController
from app.database import get_db_connection
from app.views import CategoryCreate, CategoryResponse, CategoryUpdate

router = APIRouter(prefix="/categories", tags=["Categories"])


@router.get("/", response_model=List[CategoryResponse])
def get_categories(db: sqlite3.Connection = Depends(get_db_connection)):
    return CategoryController.list_categories(db)


@router.get("/{category_id}", response_model=CategoryResponse)
def get_category(category_id: int, db: sqlite3.Connection = Depends(get_db_connection)):
    return CategoryController.get_category(db, category_id)


@router.post("/", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
def create_category(category: CategoryCreate, db: sqlite3.Connection = Depends(get_db_connection)):
    return CategoryController.create_category(db, category)


@router.put("/{category_id}", response_model=CategoryResponse)
def update_category(
    category_id: int,
    category: CategoryUpdate,
    db: sqlite3.Connection = Depends(get_db_connection),
):
    return CategoryController.update_category(db, category_id, category)


@router.delete("/{category_id}", response_model=CategoryResponse, status_code=status.HTTP_200_OK)
def delete_category(category_id: int, db: sqlite3.Connection = Depends(get_db_connection)):
    return CategoryController.delete_category(db, category_id)