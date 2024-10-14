from flask import Blueprint, render_template
from ..database import get_db_connection

bp = Blueprint("admin", __name__)


@bp.route("/players")
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


@bp.route("/choices")
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
