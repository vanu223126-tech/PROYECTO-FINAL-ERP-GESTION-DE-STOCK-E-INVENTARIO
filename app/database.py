import sqlite3
from typing import Generator


DB_NAME = "stock e inventory.db"

def get_db_connection()-> Generator[sqlite3.Connection, None, None]:

    conn = sqlite3.connect(DB_NAME, check_same_thread=False)
    conn.row_factory=sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    try:
        yield conn
    finally:
        conn.close()


def init_db() -> None:

    with sqlite3.connect(DB_NAME) as conn:
        conn.execute("PRAGMA foreign_keys = ON")
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Category (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT NOT NULL
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Supplier (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                address TEXT NOT NULL,
                phone TEXT NOT NULL,
                email TEXT NOT NULL
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS articles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT NOT NULL,
                unit_price REAL NOT NULL,
                stock INTEGER NOT NULL,
                sale_price REAL NOT NULL,
                id_Category INTEGER,
                id_Supplier INTEGER,
                FOREIGN KEY (id_Category) REFERENCES Category(id) ON DELETE CASCADE,
                FOREIGN KEY (id_Supplier) REFERENCES Supplier(id) ON DELETE CASCADE
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS customers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                address TEXT NOT NULL,
                phone TEXT NOT NULL,
                email TEXT NOT NULL,
                registration_date TEXT NOT NULL
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS branch (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                address TEXT NOT NULL,
                phone TEXT NOT NULL
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS deposit (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                address TEXT NOT NULL
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS warehouse_stock (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                id_articles INTEGER NOT NULL,
                id_deposit INTEGER NOT NULL,
                amount INTEGER NOT NULL,
                FOREIGN KEY (id_articles) REFERENCES articles(id) ON DELETE CASCADE,
                FOREIGN KEY (id_deposit) REFERENCES deposit(id) ON DELETE CASCADE
            )
        """)

        cursor.execute("""
                    CREATE TABLE IF NOT EXISTS stock_movements (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        transaction_date TEXT NOT NULL,
                        amount_moved INTEGER NOT NULL,
                        movement_type TEXT NOT NULL,
                        id_articles INTEGER NOT NULL,
                        id_deposit INTEGER NOT NULL,
                        FOREIGN KEY (id_articles) REFERENCES articles(id) ON DELETE CASCADE,
                         FOREIGN KEY (id_deposit) REFERENCES deposit(id) ON DELETE CASCADE
                    )
                """)


        cursor.execute("""
                            CREATE TABLE IF NOT EXISTS invoices (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                date TEXT NOT NULL,
                                total INTEGER NOT NULL,
                                id_customer INTEGER NOT NULL,
                                id_branch INTEGER NOT NULL,
                                FOREIGN KEY (id_customer) REFERENCES customers(id) ON DELETE CASCADE,
                                FOREIGN KEY (id_branch) REFERENCES branch(id_branch) ON DELETE CASCADE
                            )
                        """)

        cursor.execute("""
                                    CREATE TABLE IF NOT EXISTS invoice_detail (
                                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                                        amount INTEGER NOT NULL,
                                        unit_price REAL NOT NULL,
                                        id_invoice INTEGER NOT NULL,
                                        id_article INTEGER NOT NULL,
                                        FOREIGN KEY (id_invoice) REFERENCES invoices(id) ON DELETE CASCADE,
                                        FOREIGN KEY (id_article) REFERENCES articles(id) ON DELETE CASCADE
                                    )
                                """)
        
        conn.commit()

        