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


def compile_player_history(player_id, include_current_option=False):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute(
        """
        SELECT * FROM players WHERE id = %s
        """,
        (player_id,),
    )
    player = c.fetchone()
    c.execute(
        """
        SELECT * FROM choices WHERE player_id = %s
        """,
        (player_id,),
    )
    choices = c.fetchall()
    conn.close()

    history = ""
    for choice in choices:
        history += f"Hello, {player['name']}.\n"
        history += f"You are {choice['age']} years old.\n\n"
        history += f"{choice['stage_text']}\n\n"
        history += f"{choice['option_text']}\n\n"
        history += f"{choice['choice_title']}\n\n"
        history += f"{choice['choice_text']}\n\n"
        history += "Time passes...\n\n"

    history += f"Hello, {player['name']}.\n"
    history += f"You are {player['current_age']} years old.\n\n"

    if player["current_stage_text"]:
        history += f"{player['current_stage_text']}\n\n"

    if player["current_option"] and include_current_option:
        history += f"{player['current_option_text']}\n\n"

    return history
