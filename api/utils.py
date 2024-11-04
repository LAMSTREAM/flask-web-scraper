from os import environ
from flask import jsonify, abort

def json_abort(status_code, data=None):
    response = jsonify(data)
    response.status_code = status_code
    abort(response)

def safe_get_env_var(key):
    try:
        return environ[key]
    except KeyError:
        raise NameError(f"Missing {key} environment variable.")
