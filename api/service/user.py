from flask import Blueprint, request, jsonify
from sqlalchemy.exc import SQLAlchemyError
from api.security.auth import require_auth
from api.db.user import db_sync_user

bp_name = 'user'
bp_url_prefix = '/api/user'
bp = Blueprint(bp_name, __name__, url_prefix=bp_url_prefix)


@bp.route('/sync-user', methods=['POST'])
@require_auth(None)
def sync_user():
    data = request.get_json()
    sub = data.get('Auth0-sub')
    email = data.get('Auth0-email')

    # Validate input
    if not sub or not email:
        return jsonify({"error": "Missing 'Auth0-sub' or 'Auth0-email' in payload"}), 400

    try:
        # Call the sync_user function to handle database logic
        user, message = db_sync_user(sub, email)

        return jsonify({"message": message}), 200

    except SQLAlchemyError as e:
        return jsonify({"error": "Database error occurred", "details": str(e)}), 500
