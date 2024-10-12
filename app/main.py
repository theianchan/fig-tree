from flask import Flask, render_template, request, jsonify
import logging
from .config import template_dir, static_dir
from .database import get_db_connection, init_db

logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s"
)   

app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/submit_name", methods=['POST'])
def submit_name():
    try:
        data = request.json
        user_id = data.get('userId')
        name = data.get('name')

        logging.debug(f"Received name: {name}")
        logging.debug(f"Received user_id: {user_id}")
        
        conn = get_db_connection()
        c = conn.cursor()
        c.execute("INSERT OR REPLACE INTO players (id, name) VALUES (?, ?)", (user_id, name))
        conn.commit()
        conn.close()
        
        return jsonify({"success": True, "message": "Submitted successfully"})
    
    except Exception as e:
        logging.error(f"Error in submit_name: {str(e)}")
        return jsonify({"success": False, "message": "Server error"}), 500


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
