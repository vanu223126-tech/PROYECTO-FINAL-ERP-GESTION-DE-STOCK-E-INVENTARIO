import sqlite3
from typing import List
from fastapi import APIRouter, Depends, status

from app.controllers.stock_movement_controller import StockMovementController
from app.database import get_db_connection
from app.views import StockMovementCreate, StockMovementResponse

router = APIRouter(prefix="/stock-movements", tags=["Stock Movements"])


@router.get("/", response_model=List[StockMovementResponse])
def get_stock_movements(db: sqlite3.Connection = Depends(get_db_connection)):
    return StockMovementController.list_stock_movements(db)


@router.get("/{movement_id}", response_model=StockMovementResponse)
def get_stock_movement(movement_id: int, db: sqlite3.Connection = Depends(get_db_connection)):
    return StockMovementController.get_stock_movement(db, movement_id)


@router.post("/", response_model=StockMovementResponse, status_code=status.HTTP_201_CREATED)
def create_stock_movement(
    movement: StockMovementCreate, db: sqlite3.Connection = Depends(get_db_connection)
):
    return StockMovementController.create_stock_movement(db, movement)


@router.delete(
    "/{movement_id}", response_model=StockMovementResponse, status_code=status.HTTP_200_OK
)
def delete_stock_movement(movement_id: int, db: sqlite3.Connection = Depends(get_db_connection)):
    return StockMovementController.delete_stock_movement(db, movement_id)