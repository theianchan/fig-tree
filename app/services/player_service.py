from ..database import get_db_connection
from ..utils import generate_unique_id
from datetime import datetime, timezone


def get_player(player_id):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute(
        """
        SELECT * FROM players WHERE id = %s
        """,
        (player_id,),
    )
    player = c.fetchone()
    conn.close()
    return player


def create_player(name, current_option):
    player_id = generate_unique_id("player", "players")
    current_age = 21
    current_time = datetime.now(timezone.utc).isoformat()
    conn = get_db_connection()
    c = conn.cursor()
    c.execute(
        """
        INSERT INTO players (id, name, current_age, current_option, time_stage_started)
        VALUES (%s, %s, %s, %s, %s)
        ON CONFLICT (id) DO UPDATE
        SET name = EXCLUDED.name,
            current_age = EXCLUDED.current_age,
            current_option = EXCLUDED.current_option,
            time_stage_started = EXCLUDED.time_stage_started
        """,
        (
            player_id,
            name,
            current_age,
            current_option,
            current_time,
        ),
    )
    conn.commit()
    conn.close()
    return player_id


def update_player_option(player_id, current_option):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute(
        """
        UPDATE players 
        SET current_option = %s 
        WHERE id = %s
        """,
        (
            current_option,
            player_id,
        ),
    )
    conn.commit()
    conn.close()


def update_player_age(player_id):
    current_time = datetime.now(timezone.utc).isoformat()
    conn = get_db_connection()
    c = conn.cursor()
    c.execute(
        """
        UPDATE players
        SET current_age = current_age + 7,
            current_option = NULL,
            time_stage_started = %s
        WHERE id = %s
        """,
        (
            current_time,
            player_id,
        ),
    )
    conn.commit()
    conn.close()
