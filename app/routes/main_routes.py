from flask import Blueprint, render_template, request, jsonify, make_response
from ..services.player_service import *
from ..services.choice_service import *
from ..services.story_service import *
import logging

bp = Blueprint("main", __name__)


@bp.route("/")
def index():
    player_id = request.cookies.get("playerId")
    current_option = request.args.get("fig") or None

    if player_id:
        player = get_player(player_id)

        if player:
            choices = get_player_choices(player_id)

            # If the player is entering a new stage (no stage text),
            # generate new stage text and save it.
            if not player["current_stage_text"]:
                current_stage_text = generate_stage_text(player_id)
                player["current_stage_text"] = current_stage_text
                update_player_stage_text(player_id, current_stage_text)

            # If a fig was tapped, generate new option text and save it.
            if current_option:
                current_option_text = generate_option_text(player_id, current_option)
                player["current_option"] = current_option
                player["current_option_text"] = current_option_text
                update_player_option(player_id, current_option, current_option_text)

                # If the fig is the first in a stage, set the time.
                if not player["time_stage_started"]:
                    update_player_time_stage_started(player_id)

            # If a fig was NOT tapped but there is a saved current option with no text
            # (which happens on new user creation), generate new option text and save it.
            elif player["current_option"] and not player["current_option_text"]:
                current_option_text = generate_option_text(
                    player_id, player["current_option"]
                )
                player["current_option_text"] = current_option_text
                update_player_option(
                    player_id, player["current_option"], current_option_text
                )

                # Same here (inelegant, fix later)
                if not player["time_stage_started"]:
                    update_player_time_stage_started(player_id)

            else:
                pass

            # If a fig was not tapped, use the existing player values.
            # If there are no values, the template will ask the player to
            # tap a fig to continue.

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

        if not player_id:
            return jsonify({"success": False, "message": "Player not found"}), 400

        player = get_player(player_id)
        current_age = player["current_age"]
        stage_text = player["current_stage_text"]

        if committed:
            option_text = player["current_option_text"]
            choice_raw = player["current_option"]
            choice_title, choice_text = generate_choice_title_text(
                player_id, choice_raw
            )
        else:
            option_text = None
            choice_raw = "no commit"
            choice_title, choice_text = generate_no_choice_title_text(player_id)

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
