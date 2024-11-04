##########################################
# External Modules
##########################################

from flask import Flask
from flask_cors import CORS
from flask_talisman import Talisman

from api.service import user, website, analysis
from api.utils import safe_get_env_var
from api import exception_views

from api.config import Config
from api.db.models import db


def create_app():
    ##########################################
    # Environment Variables
    ##########################################
    client_origin_url = safe_get_env_var("CLIENT_ORIGIN_URL")

    ##########################################
    # Flask App Instance
    ##########################################

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(Config)

    db.init_app(app)

    ##########################################
    # HTTP Security Headers
    ##########################################

    csp = {
        'default-src': ['\'self\''],
        'frame-ancestors': ['\'none\'']
    }

    Talisman(
        app,
        force_https=False,
        frame_options='DENY',
        content_security_policy=csp,
        referrer_policy='no-referrer',
        x_xss_protection=False,
        x_content_type_options=True
    )

    @app.after_request
    def add_headers(response):
        response.headers['X-XSS-Protection'] = '0'
        response.headers['Cache-Control'] = 'no-store, max-age=0, must-revalidate'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'
        response.headers['Content-Type'] = 'application/json; charset=utf-8'
        response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
        return response

    ##########################################
    # CORS
    ##########################################

    if Config.FLASK_ENV == 'production':
        CORS(
            app,
            resources={r"/*": {"origins": client_origin_url}},
            allow_headers=["Authorization", "Content-Type"],
            # methods=["GET", "POST"],  #dependens on the methods you used
            max_age=86400
        )
    else:
        CORS(
            app,
            max_age=86400
        )


    ##########################################
    # Blueprint Registration
    ##########################################

    app.register_blueprint(exception_views.bp)
    app.register_blueprint(user.bp)
    app.register_blueprint(website.bp)
    app.register_blueprint(analysis.bp)

    @app.cli.command("init-db")
    def init_db():
        """Initialize the database."""
        db.create_all()
        print("Database initialized.")

    @app.cli.command("reset-db")
    def reset_db():
        """Initialize the database."""
        db.drop_all()
        print("Database reset.")

    return app
