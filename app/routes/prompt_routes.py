from flask import Blueprint, request, jsonify, g
from app.services.prompt_service import PromptService
from decorators import token_required
from app.services.auth_service import AuthService

auth_service = AuthService()
prompt_service = PromptService(auth_service.client)
prompt_bp = Blueprint('prompt', __name__)
@prompt_bp.route('/api/prompt', methods=['GET'])
@token_required
def get_data():
    user_id = g.user["id"]  # This assumes your decorator sets g.user
    results = prompt_service.get_prompt_data(user_id)

    return jsonify({
        "message": "User registered successfully",
        "data": results
    }), 200