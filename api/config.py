# config.py

from api.utils import safe_get_env_var

class Config:
    # Fetch the DATABASE_URL from the environment
    SQLALCHEMY_DATABASE_URI = safe_get_env_var("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    FLASK_ENV = safe_get_env_var('FLASK_ENV')
    DEBUG = safe_get_env_var('FLASK_DEBUG')
    TESTING = safe_get_env_var('FLASK_TESTING')

    HOST = safe_get_env_var('FLASK_RUN_HOST')
    PORT = int(safe_get_env_var('FLASK_RUN_PORT'))
