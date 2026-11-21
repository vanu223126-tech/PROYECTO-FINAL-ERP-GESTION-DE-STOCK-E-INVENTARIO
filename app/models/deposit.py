import sqlite3
from typing import List, Optional


class DepositModel:

    @staticmethod
    def get_all(conn: sqlite3.Connection) -> List[sqlite3.Row]:
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, address FROM deposit ORDER BY id DESC")
        return cursor.fetchall()

    @staticmethod
    def get_by_id(conn: sqlite3.Connection, deposit_id: int) -> Optional[sqlite3.Row]:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, name, address FROM deposit WHERE id = ?",
            (deposit_id,),
        )
        return cursor.fetchone()

    @staticmethod
    def create(
        conn: sqlite3.Connection,
        name: str,
        address: str,
    ) -> int:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO deposit (name, address) VALUES (?, ?)",
            (name, address),
        )
        conn.commit()
        return cursor.lastrowid

    @staticmethod
    def update(
        conn: sqlite3.Connection,
        deposit_id: int,
        name: str,
        address: str,
    ) -> bool:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE deposit SET name = ?, address = ? WHERE id = ?",
            (name, address, deposit_id),
        )
        conn.commit()
        return cursor.rowcount > 0

    @staticmethod
    def delete(conn: sqlite3.Connection, deposit_id: int) -> bool:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM deposit WHERE id = ?", (deposit_id,))
        conn.commit()
        return cursor.rowcount > 0