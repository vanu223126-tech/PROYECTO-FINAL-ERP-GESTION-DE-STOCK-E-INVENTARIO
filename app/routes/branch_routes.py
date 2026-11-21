import sqlite3
from typing import List
from fastapi import APIRouter, Depends, status

from app.controllers.branch_controller import BranchController
from app.database import get_db_connection
from app.views import BranchCreate, BranchResponse, BranchUpdate

router = APIRouter(prefix="/branches", tags=["Branches"])


@router.get("/", response_model=List[BranchResponse])
def get_branches(db: sqlite3.Connection = Depends(get_db_connection)):
    return BranchController.list_branches(db)


@router.get("/{branch_id}", response_model=BranchResponse)
def get_branch(branch_id: int, db: sqlite3.Connection = Depends(get_db_connection)):
    return BranchController.get_branch(db, branch_id)


@router.post("/", response_model=BranchResponse, status_code=status.HTTP_201_CREATED)
def create_branch(branch: BranchCreate, db: sqlite3.Connection = Depends(get_db_connection)):
    return BranchController.create_branch(db, branch)


@router.put("/{branch_id}", response_model=BranchResponse)
def update_branch(
    branch_id: int,
    branch: BranchUpdate,
    db: sqlite3.Connection = Depends(get_db_connection),
):
    return BranchController.update_branch(db, branch_id, branch)


@router.delete("/{branch_id}", response_model=BranchResponse, status_code=status.HTTP_200_OK)
def delete_branch(branch_id: int, db: sqlite3.Connection = Depends(get_db_connection)):
    return BranchController.delete_branch(db, branch_id)