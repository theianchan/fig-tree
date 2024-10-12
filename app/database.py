import sqlite3


def get_db_connection():
    conn = sqlite3.connect("players.db")
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute(
        """CREATE TABLE IF NOT EXISTS players
        (id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        age INTEGER, 
        story TEXT,
        choice_1 TEXT,
        choice_2 TEXT,
        choice_3 TEXT,
        choice_4 TEXT,
        choice_5 TEXT,
        choice_6 TEXT,
        choice_7 TEXT,
        choice_8 TEXT)"""
    )
    conn.commit()
    conn.close()
