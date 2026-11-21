import sqlite3
from typing import List
from fastapi import HTTPException, status

from app.models.deposit import DepositModel
from app.views import DepositCreate, DepositResponse, DepositUpdate


class DepositController:

    @staticmethod
    def list_deposits(db: sqlite3.Connection) -> List[DepositResponse]:
        rows = DepositModel.get_all(db)
        return [DepositResponse.model_validate(dict(row)) for row in rows]

    @staticmethod
    def get_deposit(db: sqlite3.Connection, deposit_id: int) -> DepositResponse:
        row = DepositModel.get_by_id(db, deposit_id)
        if not row:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Depósito con ID {deposit_id} no encontrado",
            )
        return DepositResponse.model_validate(dict(row))

    @staticmethod
    def create_deposit(db: sqlite3.Connection, deposit: DepositCreate) -> DepositResponse:
        try:
            new_id = DepositModel.create(
                conn=db,
                name=deposit.name,
                address=deposit.address,
            )
        except sqlite3.IntegrityError as exc:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Error de integridad al crear el depósito: {exc}",
            ) from exc

        row = DepositModel.get_by_id(db, new_id)
        return DepositResponse.model_validate(dict(row))

    @staticmethod
    def update_deposit(
        db: sqlite3.Connection, deposit_id: int, deposit: DepositUpdate
    ) -> DepositResponse:
        try:
            updated = DepositModel.update(
                conn=db,
                deposit_id=deposit_id,
                name=deposit.name,
                address=deposit.address,
            )
        except sqlite3.IntegrityError as exc:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Error de integridad al actualizar el depósito: {exc}",
            ) from exc

        if not updated:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Depósito con ID {deposit_id} no encontrado",
            )
        row = DepositModel.get_by_id(db, deposit_id)
        return DepositResponse.model_validate(dict(row))

    @staticmethod
    def delete_deposit(db: sqlite3.Connection, deposit_id: int) -> DepositResponse:
        row = DepositModel.get_by_id(db, deposit_id)
        if not row:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Depósito con ID {deposit_id} no encontrado",
            )
        response_data = DepositResponse.model_validate(dict(row))
        try:
            DepositModel.delete(db, deposit_id)
        except sqlite3.IntegrityError as exc:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="No se puede eliminar el depósito porque tiene movimientos asociados",
            ) from exc
        return response_data