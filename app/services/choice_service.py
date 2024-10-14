from ..database import get_db_connection
from ..utils import generate_unique_id


def get_player_choices(player_id):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute(
        """
        SELECT * FROM choices WHERE player_id = %s
        """,
        (player_id,),
    )
    choices = c.fetchall()
    conn.close()
    return choices


def create_player_choice(
    player_id,
    current_age,
    stage_text,
    option_text,
    choice_raw,
    choice_title,
    choice_text,
):
    choice_id = generate_unique_id("choice", "choices")
    conn = get_db_connection()
    c = conn.cursor()
    c.execute(
        """
        INSERT INTO choices (
            id,
            player_id, 
            age, 
            stage_text, 
            option_text, 
            choice_raw, 
            choice_title, 
            choice_text
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """,
        (
            choice_id,
            player_id,
            current_age,
            stage_text,
            option_text,
            choice_raw,
            choice_title,
            choice_text,
        ),
    )
    conn.commit()
    conn.close()
