import sqlite3
from typing import Generator


DB_NAME = "inventory.db"

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
            CREATE TABLE IF NOT EXISTS Categoria (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                descripcion TEXT NOT NULL
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Proveedor (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                direccion TEXT NOT NULL,
                telefono TEXT NOT NULL,
                email TEXT NOT NULL
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS articulos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                descripcion TEXT NOT NULL,
                precio_unitario REAL NOT NULL,
                Stock INTEGER NOT NULL,
                precio_venta REAL NOT NULL,
                id_Categoria INTEGER,
                id_Proveedor INTEGER,
                FOREIGN KEY (id_Categoria) REFERENCES Categoria(id) ON DELETE CASCADE,
                FOREIGN KEY (id_Proveedor) REFERENCES Proveedor(id) ON DELETE CASCADE
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS clientes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                direccion TEXT NOT NULL,
                telefono TEXT NOT NULL,
                email TEXT NOT NULL,
                fecha_registro TEXT NOT NULL
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sucursal (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre_sucursal TEXT NOT NULL,
                direccion TEXT NOT NULL,
                telefono TEXT NOT NULL
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS deposito (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                direccion TEXT NOT NULL
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS stock_deposito (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                id_articulo INTEGER NOT NULL,
                id_deposito INTEGER NOT NULL,
                cantidad INTEGER NOT NULL,
                FOREIGN KEY (id_articulo) REFERENCES articulos(id) ON DELETE CASCADE,
                FOREIGN KEY (id_deposito) REFERENCES deposito(id) ON DELETE CASCADE
            )
        """)

        cursor.execute("""
                    CREATE TABLE IF NOT EXISTS movimientos_stock (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        fecha_movimiento TEXT NOT NULL,
                        cantidad_movida INTEGER NOT NULL,
                        tipo_movimiento TEXT NOT NULL,
                        id_articulo INTEGER NOT NULL,
                        id_deposito INTEGER NOT NULL,
                        FOREIGN KEY (id_articulo) REFERENCES articulos(id_articulo) ON DELETE CASCADE,
                         FOREIGN KEY (id_deposito) REFERENCES deposito(id_Deposito) ON DELETE CASCADE
                    )
                """)


        cursor.execute("""
                            CREATE TABLE IF NOT EXISTS facturas (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                fecha TEXT NOT NULL,
                                total INTEGER NOT NULL,
                                id_clientes INTEGER NOT NULL,
                                id_sucursal INTEGER NOT NULL,
                                FOREIGN KEY (id_clientes) REFERENCES Clientes(id_clientes) ON DELETE CASCADE,
                                FOREIGN KEY (id_sucursal) REFERENCES sucursal(id_sucursal) ON DELETE CASCADE
                            )
                        """)

        cursor.execute("""
                                    CREATE TABLE IF NOT EXISTS detalle_factura (
                                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                                        cantidad INTEGER NOT NULL,
                                        precio_unitario REAL NOT NULL,
                                        id_factura INTEGER NOT NULL,
                                        id_articulo INTEGER NOT NULL,
                                        FOREIGN KEY (id_factura) REFERENCES facturas(id) ON DELETE CASCADE,
                                        FOREIGN KEY (id_articulo) REFERENCES articulos(id) ON DELETE CASCADE
                                    )
                                """)
        

        