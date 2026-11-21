from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.database import init_db
from app.routes.branch_routes import router as branch_router
from app.routes.articles_routes import router as articles_router
from app.routes.Category_routes import router as category_router
from app.routes.customer_routes import router as customer_router
from app.routes.deposit_routes import router as deposit_router
from app.routes.invoices_routes import router as invoices_router
from app.routes.stock_movements_routes import router as stock_movements_router
from app.routes.Supplier_routes import router as supplier_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app= FastAPI(
    title="stock_e_inventory API (MVC)",
    version="1.0.0",
    lifespan=lifespan
)

app.include_router(branch_router, prefix="/api/branches", tags=["Branches"])
app.include_router(articles_router, prefix="/api/articles", tags=["Articles"])
app.include_router(category_router, prefix="/api/categories", tags=["Categories"])
app.include_router(customer_router, prefix="/api/customers", tags=["Customers"])
app.include_router(deposit_router, prefix="/api/deposits", tags=["Deposits"])
app.include_router(invoices_router, prefix="/api/invoices", tags=["Invoices"])
app.include_router(stock_movements_router, prefix="/api/stock-movements", tags=["Stock Movements"])
app.include_router(supplier_router, prefix="/api/suppliers", tags=["Suppliers"])

if __name__ == "__main__":
    import importlib

    importlib.import_module("uvicorn").run(
        "main:app", host="127.0.0.1", port=8000, reload=True
    )