from flask import request, jsonify
from functools import wraps
from app.services.auth_service import AuthService
import jwt
import os

auth_service = AuthService()

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        if not token.startswith("Bearer "):
            return jsonify({'message': 'Invalid token format. Expected "Bearer <token>"'}), 401

        token = token.replace("Bearer ", "")
        try:
            decoded_token = jwt.decode(token, os.environ.get('SECRET_KEY'), algorithms=["HS256"], audience="authenticated")
            user_id = decoded_token.get('sub')
            print(f"Token jest ważny. ID użytkownika: {user_id}")
            # kwargs['user_id'] = user_id
        except jwt.ExpiredSignatureError as e:
            print(f"Token wygasł: {e}")
            return jsonify({'message': 'Token has expired!'}), 401
        except jwt.InvalidAudienceError as e:
            print(f"Nieprawidłowy odbiorca: {e}")
            return jsonify({'message': 'Invalid audience!'}), 401
        except jwt.InvalidTokenError as e:
            print(f"Nieprawidłowy token: {e}")
            return jsonify({'message': 'Invalid token!'}), 401
        except Exception as e:
            print(f"Wystąpił błąd podczas dekodowania tokenu: {e}")
            return jsonify({'message': 'Invalid token!'}), 401

        return f(*args, **kwargs)
    return decorated

