import sqlite3
from typing import List
from fastapi import APIRouter, Depends, status

from app.controllers.invoices_controller import InvoiceController
from app.database import get_db_connection
from app.views import InvoiceCreate, InvoiceResponse

router = APIRouter(prefix="/invoices", tags=["Invoices"])


@router.get("/", response_model=List[InvoiceResponse])
def get_invoices(db: sqlite3.Connection = Depends(get_db_connection)):
    return InvoiceController.list_invoices(db)


@router.get("/{invoice_id}", response_model=InvoiceResponse)
def get_invoice(invoice_id: int, db: sqlite3.Connection = Depends(get_db_connection)):
    return InvoiceController.get_invoice(db, invoice_id)


@router.post("/", response_model=InvoiceResponse, status_code=status.HTTP_201_CREATED)
def create_invoice(invoice: InvoiceCreate, db: sqlite3.Connection = Depends(get_db_connection)):
    return InvoiceController.create_invoice(db, invoice)


@router.delete("/{invoice_id}", response_model=InvoiceResponse, status_code=status.HTTP_200_OK)
def delete_invoice(invoice_id: int, db: sqlite3.Connection = Depends(get_db_connection)):
    return InvoiceController.delete_invoice(db, invoice_id)