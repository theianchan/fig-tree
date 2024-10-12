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
        last_tap TEXT,
        time_last_stage TIMESTAMP,
        choice_21 TEXT,
        choice_28 TEXT,
        choice_35 TEXT,
        choice_42 TEXT,
        choice_49 TEXT,
        choice_56 TEXT,
        choice_63 TEXT,
        choice_70 TEXT)"""
    )
    conn.commit()
    conn.close()
