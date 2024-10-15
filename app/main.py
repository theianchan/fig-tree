from flask import Flask
from .config import template_dir, static_dir
from .database import init_db
from .routes import main_routes, admin_routes
import logging


def create_app():
    app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)

    logging.basicConfig(
        level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s"
    )
    app.logger.handlers = logging.getLogger().handlers
    app.logger.debug("Initializing app")

    init_db()

    app.register_blueprint(main_routes.bp)
    app.register_blueprint(admin_routes.bp, url_prefix="/admin")

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
