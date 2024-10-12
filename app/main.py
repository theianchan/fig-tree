from flask import Flask, render_template, request, jsonify, make_response
import logging
import random
import string
from .config import template_dir, static_dir
from .database import get_db_connection, init_db
from datetime import datetime

logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s"
)

app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)


@app.route("/")
def index():
    user_id = request.cookies.get("userId")
    fig = request.args.get("fig")

    if user_id:
        conn = get_db_connection()
        c = conn.cursor()

        if fig:
            c.execute("UPDATE players SET last_tap = ? WHERE id = ?", (fig, user_id))
            conn.commit()

        c.execute("SELECT * FROM players WHERE id = ?", (user_id,))
        player = c.fetchone()
        conn.close()

        if player:
            return render_template("index.html", player=player)

    return render_template("index.html")


@app.route("/data")
def view_database():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM players")
    players = c.fetchall()
    conn.close()
    return render_template("data.html", players=players)


@app.route("/submit_name", methods=["POST"])
def submit_name():
    try:
        data = request.json
        name = data.get("name")
        user_id = generate_unique_id()
        current_time = datetime.now().isoformat()

        logging.debug(f"Received name: {name}")
        logging.debug(f"Received user_id: {user_id}")

        conn = get_db_connection()
        c = conn.cursor()
        c.execute(
            "INSERT OR REPLACE INTO players (id, name, age, time_last_stage) VALUES (?, ?, ?, ?)",
            (user_id, name, 21, current_time),
        )
        conn.commit()
        conn.close()

        response = make_response(
            jsonify({"success": True, "message": "Submitted successfully"})
        )
        response.set_cookie("userId", user_id, path="/", max_age=60 * 60 * 24 * 365)

        return response

    except Exception as e:
        logging.error(f"Error in submit_name: {str(e)}")
        return jsonify({"success": False, "message": "Server error"}), 500


@app.route("/handle_commit", methods=["POST"])
def handle_commit():
    try:
        user_id = request.cookies.get("userId")
        committed = request.json.get("committed")
        current_time = datetime.now().isoformat()

        if not user_id:
            return jsonify({"success": False, "message": "User not found"}), 400

        conn = get_db_connection()
        c = conn.cursor()
        
        c.execute("SELECT age, last_tap FROM players WHERE id = ?", (user_id,))
        player = c.fetchone()
        current_age = player['age']
        
        choice_value = player['last_tap'] if committed else "no commit"

        c.execute(
            "UPDATE players SET age = age + 7, time_last_stage = ?, choice_" + str(current_age) + " = ?, last_tap = NULL WHERE id = ?",
            (current_time, choice_value, user_id),
        )
        conn.commit()
        conn.close()

        action = "Commit" if committed else "No commit"
        return jsonify({"success": True, "message": f"{action} recorded successfully"})

    except Exception as e:
        logging.error(f"Error in handle_commit: {str(e)}")
        return jsonify({"success": False, "message": "Server error"}), 500


def generate_unique_id():
    while True:
        new_id = "player_" + "".join(
            random.choices(string.ascii_lowercase + string.digits, k=18)
        )
        conn = get_db_connection()
        c = conn.cursor()
        c.execute("SELECT id FROM players WHERE id = ?", (new_id,))
        if not c.fetchone():
            conn.close()
            return new_id
        conn.close()


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
