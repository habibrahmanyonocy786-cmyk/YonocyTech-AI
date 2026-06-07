import sqlite3
import os
from typing import Optional

DB_PATH = os.getenv("YONOCYTECH_DB_PATH") or os.path.join(
    os.path.join(os.path.dirname(__file__), "data"), "yonocytech.db"
)


def get_connection() -> sqlite3.Connection:
    db_path = os.getenv("YONOCYTECH_DB_PATH") or os.path.join(
        os.path.join(os.path.dirname(__file__), "data"), "yonocytech.db"
    )
    if db_path != ":memory:":
        os.makedirs(os.path.dirname(db_path) or ".", exist_ok=True)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    return conn


def get_db() -> sqlite3.Connection:
    return get_connection()
