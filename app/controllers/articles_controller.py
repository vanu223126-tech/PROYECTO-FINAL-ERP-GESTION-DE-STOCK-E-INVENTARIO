import sqlite3
from typing import List
from fastapi import HTTPException, status

from app.models.articles import ArticlesModel
from app.views import ArticleCreate, ArticleResponse, ArticleUpdate


class ArticleController:

    @staticmethod
    def list_articles(db: sqlite3.Connection) -> List[ArticleResponse]:
        rows = ArticlesModel.get_all(db)
        return [ArticleResponse.model_validate(dict(row)) for row in rows]

    @staticmethod
    def get_article(db: sqlite3.Connection, article_id: int) -> ArticleResponse:
        row = ArticlesModel.get_by_id(db, article_id)
        if not row:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Artículo con ID {article_id} no encontrado",
            )
        return ArticleResponse.model_validate(dict(row))

    @staticmethod
    def create_article(db: sqlite3.Connection, article: ArticleCreate) -> ArticleResponse:
        try:
            new_id = ArticlesModel.create(
                conn=db,
                name=article.name,
                description=article.description,
                unit_price=article.unit_price,
                stock=article.stock,
                sale_price=article.sale_price,
                id_Category=article.id_Category,
                id_Supplier=article.id_Supplier,
            )
        except sqlite3.IntegrityError as exc:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Error de integridad al crear el artículo (revisa categoría o proveedor): {exc}",
            ) from exc

        row = ArticlesModel.get_by_id(db, new_id)
        return ArticleResponse.model_validate(dict(row))

    @staticmethod
    def search_articles(
        db: sqlite3.Connection,
        name: str | None = None,
        description: str | None = None,
    ) -> List[ArticleResponse]:
        rows = ArticlesModel.get_all(db)
        results = []

        for row in rows:
            data = dict(row)
            if name and name.strip().lower() not in str(data.get("name", "")).lower():
                continue
            if description and description.strip().lower() not in str(data.get("description", "")).lower():
                continue
            results.append(ArticleResponse.model_validate(data))

        return results

    @staticmethod
    def update_article(
        db: sqlite3.Connection, article_id: int, article: ArticleUpdate
    ) -> ArticleResponse:
        try:
            updated = ArticlesModel.update(
                conn=db,
                article_id=article_id,
                name=article.name,
                description=article.description,
                unit_price=article.unit_price,
                stock=article.stock,
                sale_price=article.sale_price,
                id_Category=article.id_Category,
                id_Supplier=article.id_Supplier,
            )
        except sqlite3.IntegrityError as exc:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Error de integridad al actualizar el artículo: {exc}",
            ) from exc

        if not updated:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Artículo con ID {article_id} no encontrado",
            )
        row = ArticlesModel.get_by_id(db, article_id)
        return ArticleResponse.model_validate(dict(row))

    @staticmethod
    def delete_article(db: sqlite3.Connection, article_id: int) -> ArticleResponse:
        row = ArticlesModel.get_by_id(db, article_id)
        if not row:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Artículo con ID {article_id} no encontrado",
            )
        response_data = ArticleResponse.model_validate(dict(row))
        try:
            ArticlesModel.delete(db, article_id)
        except sqlite3.IntegrityError as exc:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="No se puede eliminar el artículo porque tiene registros asociados",
            ) from exc
        return response_data