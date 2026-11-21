import sqlite3
from typing import List
from fastapi import APIRouter, Depends, status

from app.controllers.customer_controller import CustomerController
from app.database import get_db_connection
from app.views import CustomerCreate, CustomerResponse, CustomerUpdate

router = APIRouter(prefix="/customers", tags=["Customers"])


@router.get("/", response_model=List[CustomerResponse])
def get_customers(db: sqlite3.Connection = Depends(get_db_connection)):
    return CustomerController.list_customers(db)


@router.get("/{customer_id}", response_model=CustomerResponse)
def get_customer(customer_id: int, db: sqlite3.Connection = Depends(get_db_connection)):
    return CustomerController.get_customer(db, customer_id)


@router.post("/", response_model=CustomerResponse, status_code=status.HTTP_201_CREATED)
def create_customer(customer: CustomerCreate, db: sqlite3.Connection = Depends(get_db_connection)):
    return CustomerController.create_customer(db, customer)


@router.put("/{customer_id}", response_model=CustomerResponse)
def update_customer(
    customer_id: int,
    customer: CustomerUpdate,
    db: sqlite3.Connection = Depends(get_db_connection),
):
    return CustomerController.update_customer(db, customer_id, customer)


@router.delete("/{customer_id}", response_model=CustomerResponse, status_code=status.HTTP_200_OK)
def delete_customer(customer_id: int, db: sqlite3.Connection = Depends(get_db_connection)):
    return CustomerController.delete_customer(db, customer_id)