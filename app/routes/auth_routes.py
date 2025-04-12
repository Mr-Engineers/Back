from flask import Blueprint, request, jsonify
from app.services.auth_service import AuthService
from decorators import token_required

auth_bp = Blueprint('auth', __name__)
auth_service = AuthService()

@auth_bp.route('/api/register', methods=['POST'])
def register():
    data = request.json
    response = auth_service.register_user(data['email'], data['password'])

    return jsonify({
        "message": "User registered successfully",
        "access_token": response.session.access_token if response.session else None,
        "user_id": response.user.id if response.user else None
    }), 200

@auth_bp.route('/api/login', methods=['POST'])
def login():
    data = request.json
    result = auth_service.login_user(data['email'], data['password'])
    if result.session.access_token:
        return jsonify({'access_token': result.session.access_token}), 200
    return jsonify({'error': 'Invalid credentials'}), 401

@auth_bp.route('/protected', methods=['GET'])
@token_required
def protected(user_id):
    return jsonify({'message': 'This is a protected endpoint'})

