
import base64
from flask import Blueprint, request, jsonify
from sqlalchemy.exc import SQLAlchemyError
from api.db.user import user_exists
from api.db.website import create_website, get_websites_by_user_sub_without_get_the_analyses, get_website_by_index_with_analyses
from api.security.auth import require_auth
from api.scrape.get_website_content_and_preview import get_website_content_and_screenshot
from api.scrape.openai_api import get_question_with_options

bp_name = 'website'
bp_url_prefix = '/api/website'
bp = Blueprint(bp_name, __name__, url_prefix=bp_url_prefix)


@bp.route('/create-website', methods=['POST'])
@require_auth(None)
def create_website_route():
    # Get JSON payload from request body
    data = request.get_json()
    sub = data.get('Auth0-sub')
    website_url = data.get('website_url')

    # Validate input
    if not sub or not website_url:
        return jsonify({"error": "Missing 'Auth0-sub' or 'website_url' in payload"}), 400

    try:
        # Check if the user exists using the new function
        if not user_exists(sub):
            return jsonify({"error": "User not found"}), 404

        # scrape the content and preview of the website
        content, screenshot = get_website_content_and_screenshot(website_url)
        question = get_question_with_options(website_content=content)

        # Call the create_website function to handle database logic
        new_website = create_website(sub, website_url, content, screenshot, question)

        return jsonify({"message": "Website created successfully", "website": {"index": new_website.index, "url": new_website.website_url}}), 201

    except SQLAlchemyError as e:
        return jsonify({"error": "Database error occurred", "details": str(e)}), 500


@bp.route('/get-websites', methods=['POST'])
@require_auth(None)
def get_websites_by_user_sub_route():
    # Get JSON payload from request body
    data = request.get_json()
    sub = data.get('Auth0-sub')

    # Check if the user exists using the new function
    if not user_exists(sub):
        return jsonify({"error": "User not found"}), 404

    try:
        # Call the get_websites_by_user_sub function to handle database logic
        websites = get_websites_by_user_sub_without_get_the_analyses(sub)

        # Format the output to exclude website_content
        website_data = [
            {
                "index": website.index,
                "website_url": website.website_url,
                "questions": website.questions,
                "ctime": website.ctime,
                "mtime": website.mtime
            }
            for website in websites
        ]

        return jsonify({"websites": website_data}), 200

    except SQLAlchemyError as e:
        return jsonify({"error": "Database error occurred", "details": str(e)}), 500


@bp.route('/get-website-by-index', methods=['POST'])
@require_auth(None)
def get_website_by_index_route():
    # Extracting data from the request
    data = request.get_json()
    sub = data.get('Auth0-sub')
    index = data.get('index')

    # Check if user exists
    if not user_exists(sub):
        return jsonify({"error": "User not found"}), 404

    try:
        # Get website data using helper function
        website = get_website_by_index_with_analyses(sub, index)
        # Convert the binary data for the website_preview to a base64 string for rendering
        website_preview_b64 = None
        if website.website_preview:
            website_preview_b64 = base64.b64encode(website.website_preview).decode('utf-8')

        # Format analyses in a serializable structure
        analyses_data = [
            {
                "index": analysis.index,
                "ctime": analysis.ctime.isoformat(),
                "question": analysis.question,
                "answer": analysis.answer
            }
            for analysis in website.analyses
        ]

        # Prepare the website data with analyses
        website_data = {
            "index": website.index,
            "ctime": website.ctime.isoformat(),
            "mtime": website.mtime.isoformat(),
            "website_url": website.website_url,
            "website_preview": website_preview_b64,
            "questions": website.questions,
            "analyses": analyses_data  # Include the analyses here
        }

        return jsonify({"website": website_data}), 200

    except SQLAlchemyError as e:
        return jsonify({"error": "Database error occurred", "details": str(e)}), 500

