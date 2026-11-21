import sqlite3
from typing import List
from fastapi import HTTPException, status

from app.models.invoices import InvoiceModel
from app.views import InvoiceCreate, InvoiceResponse


class InvoiceController:

    @staticmethod
    def list_invoices(db: sqlite3.Connection) -> List[InvoiceResponse]:
        rows = InvoiceModel.get_all(db)
        return [InvoiceResponse.model_validate(row) for row in rows]

    @staticmethod
    def get_invoice(db: sqlite3.Connection, invoice_id: int) -> InvoiceResponse:
        invoice = InvoiceModel.get_by_id(db, invoice_id)
        if not invoice:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Factura con ID {invoice_id} no encontrada",
            )
        return InvoiceResponse.model_validate(invoice)

    @staticmethod
    def create_invoice(db: sqlite3.Connection, invoice: InvoiceCreate) -> InvoiceResponse:
        items_data = [
            {"id_article": item.id_article, "amount": item.amount}
            for item in invoice.items
        ]
        try:
            invoice_id = InvoiceModel.create_transaction(
                conn=db,
                id_customer=invoice.id_customer,
                id_branch=invoice.id_branch,
                date=invoice.date,
                items=items_data,
            )
        except ValueError as exc:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(exc),
            ) from exc
        except sqlite3.IntegrityError as exc:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Error de integridad al registrar la factura: {exc}",
            ) from exc

        created = InvoiceModel.get_by_id(db, invoice_id)
        return InvoiceResponse.model_validate(created)

    @staticmethod
    def delete_invoice(db: sqlite3.Connection, invoice_id: int) -> InvoiceResponse:
        invoice = InvoiceModel.get_by_id(db, invoice_id)
        if not invoice:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Factura con ID {invoice_id} no encontrada",
            )
        response_data = InvoiceResponse.model_validate(invoice)
        try:
            InvoiceModel.delete(db, invoice_id)
        except sqlite3.IntegrityError as exc:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="No se puede eliminar la factura por restricciones de integridad",
            ) from exc
        return response_data