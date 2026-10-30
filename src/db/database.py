import sqlite3
from pathlib import Path


Database = Path(__file__).resolve().parents[2] / "users.db"


def init_db():
    conn = None
    try:
        conn = sqlite3.connect(Database)
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS products(
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            price TEXT NOT NULL,
            category TEXT NOT NULL DEFAULT 'Uncategorized'
            )
            """
        )
        product_columns = {
            column[1] for column in cursor.execute("PRAGMA table_info(products)")
        }
        if "category" not in product_columns:
            cursor.execute(
                "ALTER TABLE products "
                "ADD COLUMN category TEXT NOT NULL DEFAULT 'Uncategorized'"
            )
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            password TEXT NOT NULL
            )
            """
        )
        conn.commit()
    except sqlite3.Error as exc:
        if conn is not None:
            conn.rollback()
        raise RuntimeError(f"Database initialization failed: {exc}") from exc
    finally:
        if conn is not None:
            conn.close()
