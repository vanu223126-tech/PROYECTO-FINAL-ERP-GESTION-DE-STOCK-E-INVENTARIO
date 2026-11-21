import sqlite3
from typing import List, Optional


class StockMovementModel:

    @staticmethod
    def get_all(conn: sqlite3.Connection) -> List[sqlite3.Row]:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT
                sm.id,
                sm.transaction_date,
                sm.amount_moved,
                sm.movement_type,
                sm.id_articles,
                a.name AS article_name,
                sm.id_deposit,
                d.name AS deposit_name
            FROM stock_movements sm
            JOIN articles a ON sm.id_articles = a.id
            JOIN deposit d ON sm.id_deposit = d.id
            ORDER BY sm.id DESC
            """
        )
        return cursor.fetchall()

    @staticmethod
    def get_by_id(conn: sqlite3.Connection, movement_id: int) -> Optional[sqlite3.Row]:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT
                sm.id,
                sm.transaction_date,
                sm.amount_moved,
                sm.movement_type,
                sm.id_articles,
                a.name AS article_name,
                sm.id_deposit,
                d.name AS deposit_name
            FROM stock_movements sm
            JOIN articles a ON sm.id_articles = a.id
            JOIN deposit d ON sm.id_deposit = d.id
            WHERE sm.id = ?
            """,
            (movement_id,),
        )
        return cursor.fetchone()

    @staticmethod
    def create_transaction(
        conn: sqlite3.Connection,
        transaction_date: str,
        amount_moved: int,
        movement_type: str,
        id_articles: int,
        id_deposit: int,
    ) -> int:
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT id, name, stock FROM articles WHERE id = ?", (id_articles,))
            article = cursor.fetchone()
            if not article:
                raise ValueError(f"Artículo con ID {id_articles} no encontrado")

            cursor.execute("SELECT id FROM deposit WHERE id = ?", (id_deposit,))
            if not cursor.fetchone():
                raise ValueError(f"Depósito con ID {id_deposit} no encontrado")

            normalized_type = movement_type.strip().lower()
            if normalized_type in ("entry", "entrada", "in", "ingreso"):
                new_stock = article["stock"] + amount_moved
            elif normalized_type in ("exit", "salida", "out", "egreso"):
                if article["stock"] < amount_moved:
                    raise ValueError(f"Stock insuficiente para: {article['name']}")
                new_stock = article["stock"] - amount_moved
            else:
                raise ValueError(f"Tipo de movimiento no válido: {movement_type}")

            cursor.execute(
                """
                INSERT INTO stock_movements (
                    transaction_date,
                    amount_moved,
                    movement_type,
                    id_articles,
                    id_deposit
                )
                VALUES (?, ?, ?, ?, ?)
                """,
                (transaction_date, amount_moved, movement_type, id_articles, id_deposit),
            )
            movement_id = cursor.lastrowid

            cursor.execute(
                "UPDATE articles SET stock = ? WHERE id = ?",
                (new_stock, id_articles),
            )

            conn.commit()
            return movement_id
        except Exception:
            conn.rollback()
            raise

    @staticmethod
    def delete(conn: sqlite3.Connection, movement_id: int) -> bool:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM stock_movements WHERE id = ?", (movement_id,))
        conn.commit()
        return cursor.rowcount > 0