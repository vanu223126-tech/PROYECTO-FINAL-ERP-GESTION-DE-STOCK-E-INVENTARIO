import sqlite3
from typing import List
from fastapi import APIRouter, Depends, status

from app.controllers.deposit_controller import DepositController
from app.database import get_db_connection
from app.views import DepositCreate, DepositResponse, DepositUpdate

router = APIRouter(prefix="/deposits", tags=["Deposits"])


@router.get("/", response_model=List[DepositResponse])
def get_deposits(db: sqlite3.Connection = Depends(get_db_connection)):
    return DepositController.list_deposits(db)


@router.get("/{deposit_id}", response_model=DepositResponse)
def get_deposit(deposit_id: int, db: sqlite3.Connection = Depends(get_db_connection)):
    return DepositController.get_deposit(db, deposit_id)


@router.post("/", response_model=DepositResponse, status_code=status.HTTP_201_CREATED)
def create_deposit(deposit: DepositCreate, db: sqlite3.Connection = Depends(get_db_connection)):
    return DepositController.create_deposit(db, deposit)


@router.put("/{deposit_id}", response_model=DepositResponse)
def update_deposit(
    deposit_id: int,
    deposit: DepositUpdate,
    db: sqlite3.Connection = Depends(get_db_connection),
):
    return DepositController.update_deposit(db, deposit_id, deposit)


@router.delete("/{deposit_id}", response_model=DepositResponse, status_code=status.HTTP_200_OK)
def delete_deposit(deposit_id: int, db: sqlite3.Connection = Depends(get_db_connection)):
    return DepositController.delete_deposit(db, deposit_id)