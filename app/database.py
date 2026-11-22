from pathlib import Path
import sqlite3
import sys
from typing import Generator


def _resolve_db_path() -> str:
    if getattr(sys, "frozen", False):
        exe_dir = Path(sys.executable).resolve().parent
        exe_db = exe_dir / "stock_e_inventory.db"
        if exe_db.exists():
            return str(exe_db)

        # Fallback por si el .exe se ejecuta dentro de dist\GestionInventario
        project_root = exe_dir.parent.parent
        root_db = project_root / "stock_e_inventory.db"
        if root_db.exists():
            return str(root_db)

        return str(exe_db)

    base_dir = Path(__file__).resolve().parent
    return str(base_dir.parent / "stock_e_inventory.db")


DB_NAME = _resolve_db_path()