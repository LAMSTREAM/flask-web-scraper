
from flask import Blueprint, request, jsonify
from sqlalchemy.exc import SQLAlchemyError
from api.db.user import user_exists
from api.db.website import website_exists_for_user
from api.db.analysis import create_analysis, get_analyses_by_website
from api.security.auth import require_auth

bp_name = 'analysis'
bp_url_prefix = '/api/analysis'
bp = Blueprint(bp_name, __name__, url_prefix=bp_url_prefix)


@bp.route('/create-analysis', methods=['POST'])
@require_auth(None)
def create_analysis_route():
    # Get JSON payload from request body
    data = request.get_json()
    sub = data.get('Auth0-sub')
    website_index = data.get('website_index')
    question = data.get('analysis_question')
    answer = data.get('analysis_answer')  # Optional; can be None if not provided

    # Validate input
    if not sub or website_index is None or not question:
        return jsonify({"error": "Missing 'sub', 'website_index', or 'question' in payload"}), 400

    try:
        # Check if the user exists
        if not user_exists(sub):
            return jsonify({"error": "User not found"}), 404

        # Check if the website exists and belongs to the user
        if not website_exists_for_user(sub, website_index):
            return jsonify({"error": "Website not found or does not belong to the user"}), 404

        # Call the create_analysis function to handle database logic
        new_analysis = create_analysis(sub, website_index, question, answer)

        return jsonify({"message": "Analysis created successfully", "analysis": {
            "index": new_analysis.index,
            "question": new_analysis.question,
            "answer": new_analysis.answer,
            "ctime": new_analysis.ctime
        }}), 201

    except SQLAlchemyError as e:
        return jsonify({"error": "Database error occurred", "details": str(e)}), 500


@bp.route('/get-analyses', methods=['POST'])
@require_auth(None)
def get_analysis_route():
    # Get JSON payload from request body
    data = request.get_json()
    sub = data.get('Auth0-sub')
    website_index = data.get('website_index')

    # Validate input
    if not sub or website_index is None:
        return jsonify({"error": "Missing 'sub' or 'website_index' in payload"}), 400

    try:
        # Check if the user exists
        if not user_exists(sub):
            return jsonify({"error": "User not found"}), 404

        # Check if the website exists and belongs to the user
        if not website_exists_for_user(sub, website_index):
            return jsonify({"error": "Website not found or does not belong to the user"}), 404

        # Call the get_analyses_by_website function to handle database logic
        analyses = get_analyses_by_website(website_index)

        # Format the response
        response = [{
            "index": analysis.index,
            "question": analysis.question,
            "answer": analysis.answer,
            "ctime": analysis.ctime
        } for analysis in analyses]

        return jsonify(response), 200

    except SQLAlchemyError as e:
        return jsonify({"error": "Database error occurred", "details": str(e)}), 500
