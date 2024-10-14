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


def get_player_age(player_id):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute(
        """
        SELECT current_age FROM players WHERE id = %s
        """,
        (player_id,),
    )
    age = c.fetchone()['current_age']
    conn.close()
    return age


def create_player(name, current_option):
    player_id = generate_unique_id("player", "players")
    current_age = 21
    current_time = datetime.now(timezone.utc).isoformat()
    conn = get_db_connection()
    c = conn.cursor()
    c.execute(
        """
        INSERT INTO players (
            id,
            name,
            current_age,
            time_stage_started,
            current_option
        )
        VALUES (%s, %s, %s, %s, %s)
        """,
        (
            player_id,
            name,
            current_age,
            current_time,
            current_option,
        ),
    )
    conn.commit()
    conn.close()
    return player_id


def update_player_option(player_id, current_option, current_option_text):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute(
        """
        UPDATE players 
        SET current_option = %s,
            current_option_text = %s
        WHERE id = %s
        """,
        (
            current_option,
            current_option_text,
            player_id,
        ),
    )
    conn.commit()
    conn.close()


def update_player_stage_text(player_id, current_stage_text):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute(
        """
        UPDATE players 
        SET current_stage_text = %s 
        WHERE id = %s
        """,
        (current_stage_text, player_id),
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
            time_stage_started = %s,
            current_option = NULL,
            current_option_text = NULL
        WHERE id = %s
        """,
        (
            current_time,
            player_id,
        ),
    )
    conn.commit()
    conn.close()
