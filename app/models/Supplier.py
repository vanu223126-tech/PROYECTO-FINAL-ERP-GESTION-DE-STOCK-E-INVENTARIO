import sqlite3
from typing import List, Optional


class SupplierModel:

    @staticmethod
    def get_all(conn: sqlite3.Connection) -> List[sqlite3.Row]:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT id, name, address, phone, email
            FROM Supplier
            ORDER BY id DESC
            """
        )
        return cursor.fetchall()

    @staticmethod
    def get_by_id(conn: sqlite3.Connection, supplier_id: int) -> Optional[sqlite3.Row]:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT id, name, address, phone, email
            FROM Supplier
            WHERE id = ?
            """,
            (supplier_id,),
        )
        return cursor.fetchone()

    @staticmethod
    def create(
        conn: sqlite3.Connection,
        name: str,
        address: str,
        phone: str,
        email: str,
    ) -> int:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO Supplier (name, address, phone, email)
            VALUES (?, ?, ?, ?)
            """,
            (name, address, phone, email),
        )
        conn.commit()
        return cursor.lastrowid

    @staticmethod
    def update(
        conn: sqlite3.Connection,
        supplier_id: int,
        name: str,
        address: str,
        phone: str,
        email: str,
    ) -> bool:
        cursor = conn.cursor()
        cursor.execute(
            """
            UPDATE Supplier
            SET name = ?, address = ?, phone = ?, email = ?
            WHERE id = ?
            """,
            (name, address, phone, email, supplier_id),
        )
        conn.commit()
        return cursor.rowcount > 0

    @staticmethod
    def delete(conn: sqlite3.Connection, supplier_id: int) -> bool:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Supplier WHERE id = ?", (supplier_id,))
        conn.commit()
        return cursor.rowcount > 0