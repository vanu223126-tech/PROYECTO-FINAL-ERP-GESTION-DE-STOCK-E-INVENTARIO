from typing import Any, Dict, List, Optional, Tuple

from frontend.api_service import ArticleApiService


class ArticleService:

    @staticmethod
    def get_all() -> List[Dict[str, Any]]:
        return ArticleApiService.get_all_articles()

    @staticmethod
    def create(article_data: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
        return ArticleApiService.create_article(article_data)

    @staticmethod
    def update(article_id: int, article_data: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
        return ArticleApiService.update_article(article_id, article_data)

    @staticmethod
    def delete(article_id: int) -> Tuple[bool, Optional[str]]:
        return ArticleApiService.delete_article(article_id)