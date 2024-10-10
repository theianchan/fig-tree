from flask import Flask, session, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_caching import Cache
from models import db, User, Choice
from config import Config
import uuid

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
cache = Cache(app, config={"CACHE_TYPE": "simple"})


@app.route("/init", methods=["POST"])
def init_session():
    user_id = str(uuid.uuid4())
    new_user = User(user_id=user_id)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"user_id": user_id})


@app.route("/choice/<string:choice_type>", methods=["POST"])
@cache.memoize(50)
def make_choice(choice_type):
    user_id = request.headers.get("X-User-ID")
    user = User.query.filter_by(user_id=user_id).first()
    if not user:
        return jsonify({"error": "User not found"}), 404

    new_choice = Choice(user_id=user.user_id, choice_type=choice_type)
    db.session.add(new_choice)
    user.current_age += 7
    if user.current_age > 77:
        user.current_stage = "end"
    db.session.commit()

    # Placeholder for Claude API story generation
    story_snippet = (
        f"You made the choice: {choice_type}. Your age is now {user.current_age}."
    )

    return jsonify(
        {"message": story_snippet, "age": user.current_age, "stage": user.current_stage}
    )


@app.route("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
