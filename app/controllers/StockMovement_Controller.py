import sqlite3
from typing import List
from fastapi import HTTPException, status

from app.models.stock_movements import StockMovementModel
from app.views import StockMovementCreate, StockMovementResponse


class StockMovementController:

    @staticmethod
    def list_stock_movements(db: sqlite3.Connection) -> List[StockMovementResponse]:
        rows = StockMovementModel.get_all(db)
        return [StockMovementResponse.model_validate(dict(row)) for row in rows]

    @staticmethod
    def get_stock_movement(db: sqlite3.Connection, movement_id: int) -> StockMovementResponse:
        row = StockMovementModel.get_by_id(db, movement_id)
        if not row:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Movimiento de stock con ID {movement_id} no encontrado",
            )
        return StockMovementResponse.model_validate(dict(row))

    @staticmethod
    def create_stock_movement(
        db: sqlite3.Connection, movement: StockMovementCreate
    ) -> StockMovementResponse:
        try:
            movement_id = StockMovementModel.create_transaction(
                conn=db,
                transaction_date=movement.transaction_date,
                amount_moved=movement.amount_moved,
                movement_type=movement.movement_type,
                id_articles=movement.id_articles,
                id_deposit=movement.id_deposit,
            )
        except ValueError as exc:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(exc),
            ) from exc
        except sqlite3.IntegrityError as exc:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Error de integridad en el movimiento de stock: {exc}",
            ) from exc

        row = StockMovementModel.get_by_id(db, movement_id)
        return StockMovementResponse.model_validate(dict(row))

    @staticmethod
    def delete_stock_movement(db: sqlite3.Connection, movement_id: int) -> StockMovementResponse:
        row = StockMovementModel.get_by_id(db, movement_id)
        if not row:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Movimiento de stock con ID {movement_id} no encontrado",
            )
        response_data = StockMovementResponse.model_validate(dict(row))
        try:
            StockMovementModel.delete(db, movement_id)
        except sqlite3.IntegrityError as exc:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="No se puede eliminar el movimiento de stock por restricciones de integridad",
            ) from exc
        return response_data