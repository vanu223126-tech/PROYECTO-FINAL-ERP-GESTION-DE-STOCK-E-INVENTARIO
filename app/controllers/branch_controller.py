import sqlite3
from typing import List
from fastapi import HTTPException, status

from app.models.branch import BranchModel
from app.views import BranchCreate, BranchResponse, BranchUpdate


class BranchController:

    @staticmethod
    def list_branches(db: sqlite3.Connection) -> List[BranchResponse]:
        rows = BranchModel.get_all(db)
        return [BranchResponse.model_validate(dict(row)) for row in rows]

    @staticmethod
    def get_branch(db: sqlite3.Connection, branch_id: int) -> BranchResponse:
        row = BranchModel.get_by_id(db, branch_id)
        if not row:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Sucursal con ID {branch_id} no encontrada",
            )
        return BranchResponse.model_validate(dict(row))

    @staticmethod
    def create_branch(db: sqlite3.Connection, branch: BranchCreate) -> BranchResponse:
        try:
            new_id = BranchModel.create(
                conn=db,
                name=branch.name,
                address=branch.address,
                phone=branch.phone,
            )
        except sqlite3.IntegrityError as exc:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Error de integridad al crear la sucursal: {exc}",
            ) from exc

        row = BranchModel.get_by_id(db, new_id)
        return BranchResponse.model_validate(dict(row))

    @staticmethod
    def update_branch(
        db: sqlite3.Connection, branch_id: int, branch: BranchUpdate
    ) -> BranchResponse:
        try:
            updated = BranchModel.update(
                conn=db,
                branch_id=branch_id,
                name=branch.name,
                address=branch.address,
                phone=branch.phone,
            )
        except sqlite3.IntegrityError as exc:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Error de integridad al actualizar la sucursal: {exc}",
            ) from exc

        if not updated:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Sucursal con ID {branch_id} no encontrada",
            )
        row = BranchModel.get_by_id(db, branch_id)
        return BranchResponse.model_validate(dict(row))

    @staticmethod
    def delete_branch(db: sqlite3.Connection, branch_id: int) -> BranchResponse:
        row = BranchModel.get_by_id(db, branch_id)
        if not row:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Sucursal con ID {branch_id} no encontrada",
            )
        response_data = BranchResponse.model_validate(dict(row))
        try:
            BranchModel.delete(db, branch_id)
        except sqlite3.IntegrityError as exc:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="No se puede eliminar la sucursal porque tiene registros asociados",
            ) from exc
        return response_data