from app.views.articles_schema import ArticlesCreate, ArticlesUpdate, ArticlesResponse
from app.views.branch_schema import BranchCreate, BranchUpdate, BranchResponse
from app.views.Category_schema import CategoryCreate, CategoryUpdate, CategoryResponse
from app.views.Supplier_schema import SupplierCreate, SupplierUpdate, SupplierResponse
from app.views.customer_schema import CustomerCreate, CustomerUpdate, CustomerResponse
from app.views.deposit_schema import DepositCreate, DepositUpdate, DepositResponse
from app.views.invoices_schema import InvoiceCreate, InvoiceUpdate, InvoiceResponse
from app.views.stock_movements_schema import  StockMovementCreate, StockMovementUpdate,StockMovementResponse

__all__ = [
    "ArticlesCreate", "ArticlesUpdate", "ArticlesResponse",
    "BranchCreate", "BranchUpdate", "BranchResponse",
    "CategoryCreate", "CategoryUpdate", "CategoryResponse",
    "SupplierCreate", "SupplierUpdate", "SupplierResponse",
    "CustomerCreate", "CustomerUpdate", "CustomerResponse",
    "DepositCreate", "DepositUpdate", "DepositResponse",
    "InvoiceCreate", "InvoiceUpdate", "InvoiceResponse",
    "StockMovementCreate", "StockMovementUpdate", "StockMovementResponse",
]