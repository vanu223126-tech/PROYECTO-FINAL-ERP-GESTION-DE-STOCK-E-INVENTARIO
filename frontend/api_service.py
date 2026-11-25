from typing import Any, Dict, List, Optional, Tuple
import requests

from frontend.config import API_BASE_URL


class ArticleApiService:

    @staticmethod
    def get_all_articles() -> List[Dict[str, Any]]:
        try:
            response = requests.get(f"{API_BASE_URL}/articles/", timeout=5)
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, list):
                    return [item for item in data if isinstance(item, dict)]
                if isinstance(data, dict):
                    for key in ("items", "articles", "data", "results"):
                        if isinstance(data.get(key), list):
                            return [item for item in data[key] if isinstance(item, dict)]
            return []
        except (requests.RequestException, ValueError):
            return []

    @staticmethod
    def search_by_name(name: str) -> List[Dict[str, Any]]:
        try:
            response = requests.get(
                f"{API_BASE_URL}/articles/search",
                params={"name": name},
                timeout=5,
            )
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, list):
                    return [item for item in data if isinstance(item, dict)]
            return []
        except (requests.RequestException, ValueError):
            return []

    

    @staticmethod
    def create_article(data: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
        try:
            response = requests.post(f"{API_BASE_URL}/articles/", json=data, timeout=5)
            if response.status_code == 201:
                return True, None
            return False, response.json().get("detail", "Error al crear el artículo")
        except requests.RequestException as e:
            return False, str(e)

    @staticmethod
    def update_article(article_id: int, data: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
        try:
            response = requests.put(f"{API_BASE_URL}/articles/{article_id}", json=data, timeout=5)
            if response.status_code == 200:
                return True, None
            return False, response.json().get("detail", "Error al actualizar")
        except requests.RequestException as e:
            return False, str(e)

    @staticmethod
    def delete_article(article_id: int) -> Tuple[bool, Optional[str]]:
        try:
            response = requests.delete(f"{API_BASE_URL}/articles/{article_id}", timeout=5)
            if response.status_code in (200, 204):
                return True, None
            return False, response.json().get("detail", "Error al eliminar")
        except requests.RequestException as e:
            return False, str(e)
