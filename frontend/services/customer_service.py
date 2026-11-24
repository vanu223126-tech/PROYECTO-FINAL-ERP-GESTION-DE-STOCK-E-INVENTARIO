from typing import Any, Dict, List, Optional, Tuple
import requests

from frontend.config import API_BASE_URL

CUSTOMER_API_URL = f"{API_BASE_URL}/customers"


class CustomerService:

    @staticmethod
    def get_all() -> List[Dict[str, Any]]:
        try:
            response = requests.get(f"{CUSTOMER_API_URL}/", timeout=5)
            if response.status_code == 200:
                return response.json()
            return []
        except requests.RequestException:
            return []

    
    @staticmethod
    def search_by_email(email: str) -> Tuple[List[Dict[str, Any]], Optional[str]]:
        try:
            response = requests.get(
                f"{CUSTOMER_API_URL}/search",
                params={"email": email},
                timeout=5,
            )
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, list):
                    customers = data
                elif isinstance(data, dict) and data:
                    customers = [data]
                else:
                    customers = []

                if customers:
                    return customers, None
                return [], "Cliente no encontrado"

            try:
                detail = response.json().get("detail", "Cliente no encontrado")
            except ValueError:
                detail = "Cliente no encontrado"
            return [], detail
        except requests.RequestException as e:
            return [], str(e)
        
    @staticmethod
    def create(customer_data: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
        try:
            response = requests.post(f"{CUSTOMER_API_URL}/", json=customer_data, timeout=5)
            if response.status_code == 201:
                return True, None
            try:
                detail = response.json().get("detail", "Error al crear cliente")
            except ValueError:
                detail = "Error al crear cliente"
            return False, detail
        except requests.RequestException as e:
            return False, str(e)

    @staticmethod
    def update(customer_id: int, customer_data: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
        try:
            response = requests.put(
                f"{CUSTOMER_API_URL}/{customer_id}",
                json=customer_data,
                timeout=5,
            )
            if response.status_code == 200:
                return True, None
            try:
                detail = response.json().get("detail", "Error al actualizar cliente")
            except ValueError:
                detail = "Error al actualizar cliente"
            return False, detail
        except requests.RequestException as e:
            return False, str(e)

    @staticmethod
    def delete(customer_id: int) -> Tuple[bool, Optional[str]]:
        try:
            response = requests.delete(f"{CUSTOMER_API_URL}/{customer_id}", timeout=5)
            if response.status_code in (200, 204):
                return True, None
            try:
                detail = response.json().get("detail", "Error al eliminar cliente")
            except ValueError:
                detail = "Error al eliminar cliente"
            return False, detail
        except requests.RequestException as e:
            return False, str(e)