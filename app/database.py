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
                current_age INTEGER,
                current_option TEXT,
                time_stage_started TIMESTAMP
            );
            """
        )

        c.execute(
            """
            CREATE TABLE IF NOT EXISTS choices (
                id TEXT PRIMARY KEY,
                player_id TEXT REFERENCES players(id),
                age INTEGER,
                stage_text TEXT,
                option_text TEXT,
                choice_raw TEXT,
                choice_title TEXT,
                choice_text TEXT
            );
            """
        )

        c.execute(
            """
            CREATE OR REPLACE VIEW player_choices AS
            SELECT 
                p.id                 AS p__id,
                p.name               AS p__name,
                p.current_age        AS p__current_age,
                p.current_option     AS p__current_option,
                p.time_stage_started AS p__time_stage_started,
                c.age                AS c__age,
                c.stage_text         AS c__stage_text,
                c.option_text        AS c__option_text,
                c.choice_raw         AS c__choice_raw,
                c.choice_title       AS c__choice_title,
                c.choice_text        AS c__choice_text
            FROM 
                players p
            JOIN 
                choices c ON p.id = c.player_id
            ORDER BY 
                p.id ASC, 
                c.age ASC;
            """
        )

        conn.commit()
    except Exception as e:
        logging.error(f"Error initializing database: {e}")
    finally:
        conn.close()
