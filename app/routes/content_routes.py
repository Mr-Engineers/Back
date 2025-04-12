from flask import Blueprint, request, jsonify
from app.services.content_service import ContentService
from decorators import token_required

content_bp = Blueprint('content', __name__)
content_service = ContentService()

@content_bp.route('/api/content', methods=['GET'])
@token_required
def get_contents():
    user_id = request.user["user_id"]
    content = content_service.get_content(user_id)

    return jsonify({
        "Content": content,

    }), 200

@content_bp.route('/api/content', methods=['POST'])
@token_required
def add_content():
    user_id = request.user["user_id"]
    data = request.get_json()

    content = content_service.add_content(user_id, data)

    return jsonify({
        "Success": "Successfully added content",

    }), 200