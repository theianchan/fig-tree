from flask import Blueprint, render_template, request, jsonify, make_response
from ..services.player_service import (
    update_player_option,
    get_player,
    create_player,
    update_player_age,
)
from ..services.choice_service import get_player_choices, create_player_choice
import logging

bp = Blueprint("main", __name__)


@bp.route("/")
def index():
    player_id = request.cookies.get("playerId")
    current_option = request.args.get("fig") or None

    if player_id:
        if current_option:
            update_player_option(player_id, current_option)

        player = get_player(player_id)
        choices = get_player_choices(player_id)

        if player:
            return render_template("index.html", player=player, choices=choices)

    # For new players, write the value of `current_option` to the template.
    # This won't otherwise be preserved since we strip parameters via JS on load.
    return render_template("index.html", current_option=current_option)


@bp.route("/submit_name", methods=["POST"])
def submit_name():
    try:
        data = request.json

        name = data.get("name")
        current_option = (
            data.get("current_option") if data.get("current_option") != "None" else None
        )

        player_id = create_player(name, current_option)

        response = make_response(
            jsonify({"success": True, "message": "Submitted successfully"})
        )
        response.set_cookie("playerId", player_id, path="/", max_age=60 * 60 * 24 * 365)
        return response

    except Exception as e:
        logging.error(f"Error in submit_name: {str(e)}")
        return jsonify({"success": False, "message": "Server error"}), 500


@bp.route("/handle_commit", methods=["POST"])
def handle_commit():
    try:
        player_id = request.cookies.get("playerId")
        committed = request.json.get("committed")

        stage_text = (
            request.json.get("stage_text") or "You see a world full of possibility."
        )
        option_text = (
            request.json.get("option_text") or "Is this the right time for this choice?"
        )

        if not player_id:
            return jsonify({"success": False, "message": "Player not found"}), 400

        player = get_player(player_id)
        current_age = player["current_age"]

        if committed:
            choice_raw = player["current_option"]
            choice_title = request.json.get("choice_title") or "You make your choice."
            choice_text = request.json.get("choice_text") or "You move forward boldly."
        else:
            choice_raw = "no commit"
            choice_title = "You don't make a choice."
            choice_text = "You hesitate waiting for something better."

        update_player_age(player_id)
        create_player_choice(
            player_id,
            current_age,
            stage_text,
            option_text,
            choice_raw,
            choice_title,
            choice_text,
        )

        action = "Commit" if committed else "No commit"
        return jsonify({"success": True, "message": f"{action} recorded successfully"})

    except Exception as e:
        logging.error(f"Error in handle_commit: {str(e)}")
        return jsonify({"success": False, "message": "Server error"}), 500
