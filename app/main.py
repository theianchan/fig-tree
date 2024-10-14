from flask import Flask, render_template, request, jsonify, make_response, url_for
import logging
import random
import string
from .config import template_dir, static_dir
from .database import get_db_connection, init_db
from datetime import datetime, timezone


def create_app():
    app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)

    logging.basicConfig(
        level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s"
    )
    app.logger.handlers = logging.getLogger().handlers
    app.logger.debug("Initializing app")

    init_db()
    return app


app = create_app()


@app.route("/")
def index():
    player_id = request.cookies.get("playerId")
    current_option = request.args.get("fig") or None

    if player_id:
        conn = get_db_connection()
        c = conn.cursor()

        if current_option:
            # Set current_option based on the tapped fig.
            c.execute(
                """
                UPDATE players
                SET current_option = %s
                WHERE id = %s
                """,
                (current_option, player_id),
            )
            conn.commit()

        # Get the player's information, including past choices.
        c.execute(
            """
            SELECT *
            FROM players
            WHERE id = %s
            """,
            (player_id,),
        )
        player = c.fetchone()

        c.execute(
            """
            SELECT *
            FROM choices
            WHERE player_id = %s
            """,
            (player_id,),
        )
        choices = c.fetchall()

        conn.close()

        if player:
            return render_template("index.html", player=player, choices=choices)

    # For new players, write the value of `current_option` to the template.
    # This won't otherwise be preserved since we strip parameters via JS on load.
    return render_template("index.html", current_option=current_option)


@app.route("/players")
def view_players():
    conn = get_db_connection()
    c = conn.cursor()

    c.execute(
        """
        SELECT *
        FROM players
        """
    )
    players = c.fetchall()

    conn.close()
    return render_template("data.html", data=players)


@app.route("/choices")
def view_choices():
    conn = get_db_connection()
    c = conn.cursor()

    c.execute(
        """
        SELECT *
        FROM player_choices
        """
    )
    player_choices = c.fetchall()

    conn.close()
    return render_template("data.html", data=player_choices)


@app.route("/submit_name", methods=["POST"])
def submit_name():
    try:
        data = request.json
        id = generate_unique_id("player", "players")
        name = data.get("name")
        current_age = 21
        current_option = data.get("current_option") if data.get("current_option") != "None" else None
        current_time = datetime.now(timezone.utc).isoformat()

        conn = get_db_connection()
        c = conn.cursor()

        # Create a new player and set age to 21.
        # If the ID already exists (which shouldn't happen
        # because `generate_unique_id` checks the database),
        # overwrite the existing record.
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
            (id, name, current_age, current_option, current_time),
        )
        conn.commit()
        conn.close()

        response = make_response(
            jsonify({"success": True, "message": "Submitted successfully"})
        )
        response.set_cookie("playerId", id, path="/", max_age=60 * 60 * 24 * 365)

        return response

    except Exception as e:
        logging.error(f"Error in submit_name: {str(e)}")
        return jsonify({"success": False, "message": "Server error"}), 500


@app.route("/handle_commit", methods=["POST"])
def handle_commit():
    try:
        player_id = request.cookies.get("playerId")
        choice_id = generate_unique_id("choice", "choices")
        committed = request.json.get("committed")

        stage_text = request.json.get("stage_text") or "You see a world full of possibility."
        option_text = request.json.get("option_text") or "Is this the right time for this choice?"

        current_time = datetime.now(timezone.utc).isoformat()

        if not player_id:
            return jsonify({"success": False, "message": "Player not found"}), 400

        conn = get_db_connection()
        c = conn.cursor()

        # Get the player's current age and option.
        c.execute(
            """
            SELECT 
                current_age, 
                current_option
            FROM players
            WHERE id = %s
            """,
            (player_id,),
        )
        player = c.fetchone()

        current_age = player["current_age"]

        if committed:
            choice_raw = player["current_option"] 
            choice_title = request.json.get("choice_title") or "You make your choice."
            choice_text = request.json.get("choice_text") or "You move forward boldly."
        else:
            choice_raw = "no commit"
            choice_title = "You don't make a choice."
            choice_text = "You hesitate waiting for something better."

        # Update the player's age and clear current option.
        c.execute(
            f"""
            UPDATE players
            SET current_age = current_age + 7,
                current_option = NULL,
                time_stage_started = %s
            WHERE id = %s
            """,
            (current_time, player_id),
        )

        # Record the player's choice.
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

        action = "Commit" if committed else "No commit"
        return jsonify({"success": True, "message": f"{action} recorded successfully"})

    except Exception as e:
        logging.error(f"Error in handle_commit: {str(e)}")
        return jsonify({"success": False, "message": "Server error"}), 500


def generate_unique_id(object_name, object_table):
    while True:
        new_id = f"{object_name}_" + "".join(
            random.choices(string.ascii_lowercase + string.digits, k=18)
        )
        conn = get_db_connection()
        c = conn.cursor()

        # Check if the generated ID already exists.
        c.execute(
            f"""
            SELECT id
            FROM {object_table}
            WHERE id = %s
            """,
            (new_id,)
        )

        if not c.fetchone():
            conn.close()
            return new_id
        conn.close()


if __name__ == "__main__":
    app.run(debug=True)
