import sqlite3
from typing import List
from fastapi import APIRouter, Depends, status

from app.controllers.Supplier_Controller import SupplierController
from app.database import get_db_connection
from app.views import SupplierCreate, SupplierResponse, SupplierUpdate

router = APIRouter(prefix="/suppliers", tags=["Suppliers"])


@router.get("/", response_model=List[SupplierResponse])
def get_suppliers(db: sqlite3.Connection = Depends(get_db_connection)):
    return SupplierController.list_suppliers(db)


@router.get("/{supplier_id}", response_model=SupplierResponse)
def get_supplier(supplier_id: int, db: sqlite3.Connection = Depends(get_db_connection)):
    return SupplierController.get_supplier(db, supplier_id)


@router.post("/", response_model=SupplierResponse, status_code=status.HTTP_201_CREATED)
def create_supplier(supplier: SupplierCreate, db: sqlite3.Connection = Depends(get_db_connection)):
    return SupplierController.create_supplier(db, supplier)


@router.put("/{supplier_id}", response_model=SupplierResponse)
def update_supplier(
    supplier_id: int,
    supplier: SupplierUpdate,
    db: sqlite3.Connection = Depends(get_db_connection),
):
    return SupplierController.update_supplier(db, supplier_id, supplier)


@router.delete("/{supplier_id}", response_model=SupplierResponse, status_code=status.HTTP_200_OK)
def delete_supplier(supplier_id: int, db: sqlite3.Connection = Depends(get_db_connection)):
    return SupplierController.delete_supplier(db, supplier_id)