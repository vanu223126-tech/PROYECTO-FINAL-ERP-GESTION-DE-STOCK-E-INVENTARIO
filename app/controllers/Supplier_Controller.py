import sqlite3
from typing import List
from fastapi import HTTPException, status

from app.models.Supplier import SupplierModel
from app.views import SupplierCreate, SupplierResponse, SupplierUpdate


class SupplierController:

    @staticmethod
    def list_suppliers(db: sqlite3.Connection) -> List[SupplierResponse]:
        rows = SupplierModel.get_all(db)
        return [SupplierResponse.model_validate(dict(row)) for row in rows]

    @staticmethod
    def get_supplier(db: sqlite3.Connection, supplier_id: int) -> SupplierResponse:
        row = SupplierModel.get_by_id(db, supplier_id)
        if not row:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Proveedor con ID {supplier_id} no encontrado",
            )
        return SupplierResponse.model_validate(dict(row))

    @staticmethod
    def create_supplier(db: sqlite3.Connection, supplier: SupplierCreate) -> SupplierResponse:
        new_id = SupplierModel.create(
            conn=db,
            name=supplier.name,
            address=supplier.address,
            phone=supplier.phone,
            email=supplier.email,
        )
        row = SupplierModel.get_by_id(db, new_id)
        return SupplierResponse.model_validate(dict(row))

    @staticmethod
    def update_supplier(
        db: sqlite3.Connection, supplier_id: int, supplier: SupplierUpdate
    ) -> SupplierResponse:
        updated = SupplierModel.update(
            conn=db,
            supplier_id=supplier_id,
            name=supplier.name,
            address=supplier.address,
            phone=supplier.phone,
            email=supplier.email,
        )
        if not updated:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Proveedor con ID {supplier_id} no encontrado",
            )
        row = SupplierModel.get_by_id(db, supplier_id)
        return SupplierResponse.model_validate(dict(row))

    @staticmethod
    def delete_supplier(db: sqlite3.Connection, supplier_id: int) -> SupplierResponse:
        row = SupplierModel.get_by_id(db, supplier_id)
        if not row:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Proveedor con ID {supplier_id} no encontrado",
            )
        response_data = SupplierResponse.model_validate(dict(row))
        try:
            SupplierModel.delete(db, supplier_id)
        except sqlite3.IntegrityError as exc:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="No se puede eliminar el proveedor porque tiene registros asociados",
            ) from exc
        return response_data