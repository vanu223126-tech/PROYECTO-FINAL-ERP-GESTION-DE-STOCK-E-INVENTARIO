from typing import Any, Dict, List, Optional, Tuple
import requests

from frontend.config import API_BASE_URL

INVOICE_API_URL = f"{API_BASE_URL}/invoices"


class InvoiceService:

    @staticmethod
    def get_all() -> List[Dict[str, Any]]:
        try:
            response = requests.get(f"{INVOICE_API_URL}/", timeout=5)
            if response.status_code == 200:
                return response.json()
            return []
        except requests.RequestException:
            return []

    @staticmethod
    def create_invoice(invoice_payload: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
        try:
            response = requests.post(f"{INVOICE_API_URL}/", json=invoice_payload, timeout=5)
            if response.status_code in (200, 201):
                return True, None
            try:
                detail = response.json().get("detail", "Error al procesar la factura")
            except ValueError:
                detail = "Error al procesar la factura"
            return False, detail
        except requests.RequestException as e:
            return False, str(e)