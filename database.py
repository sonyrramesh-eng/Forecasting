import sqlite3
from contextlib import contextmanager
from .config import DATABASE_PATH

def get_connection():
    DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DATABASE_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

@contextmanager
def connection():
    conn = get_connection()
    try:
        yield conn
    finally:
        conn.close()
