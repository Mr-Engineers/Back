from flask import Blueprint, request, jsonify

from app.services.user_service import UserService
from decorators import token_required

user_bp = Blueprint('user', __name__)
user_service = UserService()

@user_bp.route('/api/user', methods=['GET'])
@token_required
def get_user():
    email = request.user["email"]
    user_id = request.user["user_id"]
    if not email:
        return jsonify({"error": "Email not found in token"}), 400
    user = user_service.get_user_by_email(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    return jsonify({
        "user": user,

    }), 200