import sqlite3

DB_NAME = "app.db"


def connect():
    return sqlite3.connect(DB_NAME)


def create_table():
    with connect() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                email TEXT NOT NULL
            )
        """)
        conn.commit()