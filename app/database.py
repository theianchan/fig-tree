import logging
import psycopg2
from psycopg2.extras import RealDictCursor
from app.config import DATABASE_URL, USE_SSL


def get_db_connection():
    conn_params = {"dsn": DATABASE_URL}
    if USE_SSL:
        conn_params["sslmode"] = "require"

    conn = psycopg2.connect(**conn_params)
    conn.cursor_factory = RealDictCursor
    return conn


def init_db():
    conn = get_db_connection()
    try:
        c = conn.cursor()
        c.execute(
            """
            CREATE TABLE IF NOT EXISTS players (
                id TEXT PRIMARY KEY,
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
                choice_70 TEXT
            )
            """
        )
        conn.commit()
    except Exception as e:
        logging.error(f"Error initializing database: {e}")
    finally:
        conn.close()
