from flask import Flask, render_template, request, jsonify, make_response
import logging
import random
import string
from .config import template_dir, static_dir
from .database import get_db_connection, init_db

logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s"
)

app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)


@app.route("/")
def index():
    user_id = request.cookies.get("userId")
    if user_id:
        conn = get_db_connection()
        c = conn.cursor()
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

        logging.debug(f"Received name: {name}")
        logging.debug(f"Received user_id: {user_id}")

        conn = get_db_connection()
        c = conn.cursor()
        c.execute(
            "INSERT OR REPLACE INTO players (id, name, age) VALUES (?, ?, ?)", (user_id, name, 21)
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


@app.route("/commit", methods=["POST"])
def commit():
    try:
        user_id = request.cookies.get("userId")
        if not user_id:
            return jsonify({"success": False, "message": "User not found"}), 400

        conn = get_db_connection()
        c = conn.cursor()
        c.execute("UPDATE players SET age = age + 7 WHERE id = ?", (user_id,))
        conn.commit()
        conn.close()

        return jsonify({"success": True, "message": "Age updated successfully"})
    
    except Exception as e:
        logging.error(f"Error in commit: {str(e)}")
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
