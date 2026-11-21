import sqlite3
from typing import Any, Dict, List, Optional


class InvoiceModel:

    @staticmethod
    def get_all(conn: sqlite3.Connection) -> List[Dict[str, Any]]:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT id, date, total, id_customer, id_branch
            FROM invoices
            ORDER BY id DESC
            """
        )
        rows = [dict(row) for row in cursor.fetchall()]

        for inv in rows:
            cursor.execute(
                """
                SELECT
                    d.id,
                    d.id_invoice,
                    d.id_article,
                    a.name AS article_name,
                    d.amount,
                    d.unit_price,
                    (d.amount * d.unit_price) AS subtotal
                FROM invoice_detail d
                JOIN articles a ON d.id_article = a.id
                WHERE d.id_invoice = ?
                """,
                (inv["id"],),
            )
            inv["items"] = [dict(detail) for detail in cursor.fetchall()]

        return rows

    @staticmethod
    def get_by_id(conn: sqlite3.Connection, invoice_id: int) -> Optional[Dict[str, Any]]:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT id, date, total, id_customer, id_branch
            FROM invoices
            WHERE id = ?
            """,
            (invoice_id,),
        )
        row = cursor.fetchone()
        if not row:
            return None

        invoice = dict(row)
        cursor.execute(
            """
            SELECT
                d.id,
                d.id_invoice,
                d.id_article,
                a.name AS article_name,
                d.amount,
                d.unit_price,
                (d.amount * d.unit_price) AS subtotal
            FROM invoice_detail d
            JOIN articles a ON d.id_article = a.id
            WHERE d.id_invoice = ?
            """,
            (invoice_id,),
        )
        invoice["items"] = [dict(detail) for detail in cursor.fetchall()]
        return invoice

    @staticmethod
    def create_transaction(
        conn: sqlite3.Connection,
        id_customer: int,
        id_branch: int,
        date: str,
        items: List[Dict[str, Any]],
    ) -> int:
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT id FROM customers WHERE id = ?", (id_customer,))
            if not cursor.fetchone():
                raise ValueError(f"Cliente con ID {id_customer} no encontrado")

            cursor.execute("SELECT id FROM branch WHERE id = ?", (id_branch,))
            if not cursor.fetchone():
                raise ValueError(f"Sucursal con ID {id_branch} no encontrada")

            total = 0.0
            processed_items = []

            for item in items:
                cursor.execute(
                    "SELECT id, name, sale_price, stock FROM articles WHERE id = ?",
                    (item["id_article"],),
                )
                article = cursor.fetchone()
                if not article:
                    raise ValueError(f"Artículo con ID {item['id_article']} no existe")

                amount = item["amount"]
                if article["stock"] < amount:
                    raise ValueError(f"Stock insuficiente para: {article['name']}")

                unit_price = article["sale_price"]
                subtotal = unit_price * amount
                total += subtotal
                processed_items.append(
                    {
                        "id_article": item["id_article"],
                        "amount": amount,
                        "unit_price": unit_price,
                    }
                )

            cursor.execute(
                """
                INSERT INTO invoices (date, total, id_customer, id_branch)
                VALUES (?, ?, ?, ?)
                """,
                (date, total, id_customer, id_branch),
            )
            invoice_id = cursor.lastrowid

            for p_item in processed_items:
                cursor.execute(
                    """
                    INSERT INTO invoice_detail (amount, unit_price, id_invoice, id_article)
                    VALUES (?, ?, ?, ?)
                    """,
                    (
                        p_item["amount"],
                        p_item["unit_price"],
                        invoice_id,
                        p_item["id_article"],
                    ),
                )
                cursor.execute(
                    "UPDATE articles SET stock = stock - ? WHERE id = ?",
                    (p_item["amount"], p_item["id_article"]),
                )

            conn.commit()
            return invoice_id
        except Exception:
            conn.rollback()
            raise

    @staticmethod
    def delete(conn: sqlite3.Connection, invoice_id: int) -> bool:
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM invoice_detail WHERE id_invoice = ?", (invoice_id,))
            cursor.execute("DELETE FROM invoices WHERE id = ?", (invoice_id,))
            deleted = cursor.rowcount > 0
            conn.commit()
            return deleted
        except Exception:
            conn.rollback()
            raise