import sqlite3
from typing import List
from fastapi import HTTPException, status

from app.models.Category import CategoryModel
from app.views import CategoryCreate, CategoryResponse, CategoryUpdate


class CategoryController:

    @staticmethod
    def list_categories(db: sqlite3.Connection) -> List[CategoryResponse]:
        rows = CategoryModel.get_all(db)
        return [CategoryResponse.model_validate(dict(row)) for row in rows]

    @staticmethod
    def get_category(db: sqlite3.Connection, category_id: int) -> CategoryResponse:
        row = CategoryModel.get_by_id(db, category_id)
        if not row:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Categoría con ID {category_id} no encontrada",
            )
        return CategoryResponse.model_validate(dict(row))

    @staticmethod
    def create_category(db: sqlite3.Connection, category: CategoryCreate) -> CategoryResponse:
        new_id = CategoryModel.create(
            conn=db,
            name=category.name,
            description=category.description,
        )
        row = CategoryModel.get_by_id(db, new_id)
        return CategoryResponse.model_validate(dict(row))

    @staticmethod
    def update_category(
        db: sqlite3.Connection, category_id: int, category: CategoryUpdate
    ) -> CategoryResponse:
        updated = CategoryModel.update(
            conn=db,
            category_id=category_id,
            name=category.name,
            description=category.description,
        )
        if not updated:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Categoría con ID {category_id} no encontrada",
            )
        row = CategoryModel.get_by_id(db, category_id)
        return CategoryResponse.model_validate(dict(row))

    @staticmethod
    def delete_category(db: sqlite3.Connection, category_id: int) -> CategoryResponse:
        row = CategoryModel.get_by_id(db, category_id)
        if not row:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Categoría con ID {category_id} no encontrada",
            )
        response_data = CategoryResponse.model_validate(dict(row))
        try:
            CategoryModel.delete(db, category_id)
        except sqlite3.IntegrityError as exc:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="No se puede eliminar la categoría porque tiene registros asociados",
            ) from exc
        return response_data