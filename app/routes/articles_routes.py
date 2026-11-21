import sqlite3
from typing import List
from fastapi import APIRouter, Depends, status

from app.controllers.articles_controller import ArticleController
from app.database import get_db_connection
from app.views import ArticleCreate, ArticleResponse, ArticleUpdate

router = APIRouter(prefix="/articles", tags=["Articles"])


@router.get("/", response_model=List[ArticleResponse])
def get_articles(db: sqlite3.Connection = Depends(get_db_connection)):
    return ArticleController.list_articles(db)


@router.get("/{article_id}", response_model=ArticleResponse)
def get_article(article_id: int, db: sqlite3.Connection = Depends(get_db_connection)):
    return ArticleController.get_article(db, article_id)


@router.post("/", response_model=ArticleResponse, status_code=status.HTTP_201_CREATED)
def create_article(article: ArticleCreate, db: sqlite3.Connection = Depends(get_db_connection)):
    return ArticleController.create_article(db, article)


@router.put("/{article_id}", response_model=ArticleResponse)
def update_article(
    article_id: int,
    article: ArticleUpdate,
    db: sqlite3.Connection = Depends(get_db_connection),
):
    return ArticleController.update_article(db, article_id, article)


@router.delete("/{article_id}", response_model=ArticleResponse, status_code=status.HTTP_200_OK)
def delete_article(article_id: int, db: sqlite3.Connection = Depends(get_db_connection)):
    return ArticleController.delete_article(db, article_id)