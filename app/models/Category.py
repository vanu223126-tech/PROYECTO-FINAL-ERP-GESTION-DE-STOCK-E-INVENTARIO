import sqlite3
from typing import List, Optional


class CategoryModel:

    @staticmethod
    def get_all(conn: sqlite3.Connection) -> List[sqlite3.Row]:
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, description FROM Category ORDER BY id DESC")
        return cursor.fetchall()

    @staticmethod
    def get_by_id(conn: sqlite3.Connection, category_id: int) -> Optional[sqlite3.Row]:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, name, description FROM Category WHERE id = ?",
            (category_id,),
        )
        return cursor.fetchone()

    @staticmethod
    def create(
        conn: sqlite3.Connection,
        name: str,
        description: str,
    ) -> int:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO Category (name, description) VALUES (?, ?)",
            (name, description),
        )
        conn.commit()
        return cursor.lastrowid

    @staticmethod
    def update(
        conn: sqlite3.Connection,
        category_id: int,
        name: str,
        description: str,
    ) -> bool:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE Category SET name = ?, description = ? WHERE id = ?",
            (name, description, category_id),
        )
        conn.commit()
        return cursor.rowcount > 0

    @staticmethod
    def delete(conn: sqlite3.Connection, category_id: int) -> bool:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Category WHERE id = ?", (category_id,))
        conn.commit()
        return cursor.rowcount > 0