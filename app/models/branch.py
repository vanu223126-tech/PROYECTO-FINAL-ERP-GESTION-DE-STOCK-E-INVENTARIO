import sqlite3
from typing import List, Optional


class BranchModel:

    @staticmethod
    def get_all(conn: sqlite3.Connection) -> List[sqlite3.Row]:
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, address, phone FROM branch ORDER BY id DESC")
        return cursor.fetchall()

    @staticmethod
    def get_by_id(conn: sqlite3.Connection, branch_id: int) -> Optional[sqlite3.Row]:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, name, address, phone FROM branch WHERE id = ?",
            (branch_id,),
        )
        return cursor.fetchone()

    @staticmethod
    def create(
        conn: sqlite3.Connection,
        name: str,
        address: str,
        phone: str,
    ) -> int:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO branch (name, address, phone) VALUES (?, ?, ?)",
            (name, address, phone),
        )
        conn.commit()
        return cursor.lastrowid

    @staticmethod
    def update(
        conn: sqlite3.Connection,
        branch_id: int,
        name: str,
        address: str,
        phone: str,
    ) -> bool:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE branch SET name = ?, address = ?, phone = ? WHERE id = ?",
            (name, address, phone, branch_id),
        )
        conn.commit()
        return cursor.rowcount > 0

    @staticmethod
    def delete(conn: sqlite3.Connection, branch_id: int) -> bool:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM branch WHERE id = ?", (branch_id,))
        conn.commit()
        return cursor.rowcount > 0