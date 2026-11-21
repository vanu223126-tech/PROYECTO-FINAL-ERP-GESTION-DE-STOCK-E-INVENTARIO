import sqlite3
from typing import List, Optional


class CustomerModel:

    @staticmethod
    def get_all(conn: sqlite3.Connection) -> List[sqlite3.Row]:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT id, name, address, phone, email, registration_date
            FROM customers
            ORDER BY id DESC
            """
        )
        return cursor.fetchall()

    @staticmethod
    def get_by_id(conn: sqlite3.Connection, customer_id: int) -> Optional[sqlite3.Row]:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT id, name, address, phone, email, registration_date
            FROM customers
            WHERE id = ?
            """,
            (customer_id,),
        )
        return cursor.fetchone()

    @staticmethod
    def create(
        conn: sqlite3.Connection,
        name: str,
        address: str,
        phone: str,
        email: str,
        registration_date: str,
    ) -> int:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO customers (name, address, phone, email, registration_date)
            VALUES (?, ?, ?, ?, ?)
            """,
            (name, address, phone, email, registration_date),
        )
        conn.commit()
        return cursor.lastrowid

    @staticmethod
    def update(
        conn: sqlite3.Connection,
        customer_id: int,
        name: str,
        address: str,
        phone: str,
        email: str,
        registration_date: str,
    ) -> bool:
        cursor = conn.cursor()
        cursor.execute(
            """
            UPDATE customers
            SET name = ?, address = ?, phone = ?, email = ?, registration_date = ?
            WHERE id = ?
            """,
            (name, address, phone, email, registration_date, customer_id),
        )
        conn.commit()
        return cursor.rowcount > 0

    @staticmethod
    def delete(conn: sqlite3.Connection, customer_id: int) -> bool:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM customers WHERE id = ?", (customer_id,))
        conn.commit()
        return cursor.rowcount > 0