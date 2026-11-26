import sqlite3
from typing import List, Optional


class ArticlesModel:

    @staticmethod
    def get_all(conn: sqlite3.Connection) -> List[sqlite3.Row]:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, name, description, unit_price, stock, sale_price, id_Category, id_Supplier FROM articles ORDER BY id DESC"
        )
        return cursor.fetchall()

    @staticmethod
    def get_by_id(conn: sqlite3.Connection, article_id: int) -> Optional[sqlite3.Row]:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, name, description, unit_price, stock, sale_price, id_Category, id_Supplier FROM articles WHERE id = ?",
            (article_id,),
        )
        return cursor.fetchone()

    @staticmethod
    def create(
        conn: sqlite3.Connection,
        name: str,
        description: str,
        unit_price: float,
        stock: int,
        sale_price: float,
        id_Category: Optional[int] = None,
        id_Supplier: Optional[int] = None,
    ) -> int:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO articles (name, description, unit_price, stock, sale_price, id_Category, id_Supplier) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (name, description, unit_price, stock, sale_price, id_Category, id_Supplier),
        )
        conn.commit()
        return cursor.lastrowid


    @staticmethod
    def search_by_name(conn: sqlite3.Connection, name: str) -> List[sqlite3.Row]:
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT id, name, description, unit_price, stock, sale_price, id_Category, id_Supplier
        FROM articles
        WHERE LOWER(name) LIKE LOWER(?)
        ORDER BY name ASC
        """,
        (f"%{name.strip()}%",),
    )
    return cursor.fetchall()
    search_articles del controller se deja como está: ya decide entre search_by_name y get_all.
    

    @staticmethod
    def update(
        conn: sqlite3.Connection,
        article_id: int,
        name: str,
        description: str,
        unit_price: float,
        stock: int,
        sale_price: float,
        id_Category: Optional[int] = None,
        id_Supplier: Optional[int] = None,
    ) -> bool:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE articles SET name = ?, description = ?, unit_price = ?, stock = ?, sale_price = ?, id_Category = ?, id_Supplier = ? WHERE id = ?",
            (name, description, unit_price, stock, sale_price, id_Category, id_Supplier, article_id),
        )
        conn.commit()
        return cursor.rowcount > 0

    @staticmethod
    def delete(conn: sqlite3.Connection, article_id: int) -> bool:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM articles WHERE id = ?", (article_id,))
        conn.commit()
        return cursor.rowcount > 0