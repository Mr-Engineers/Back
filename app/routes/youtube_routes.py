from flask import Blueprint, request, jsonify

from app.services.youtube_service import YoutubeService
from decorators import token_required


youtube_bp = Blueprint('youtube', __name__)
youtube_service = YoutubeService()

@youtube_bp.route('/api/youtube', methods=['GET'])
@token_required
def get_data():
    date_range = request.args.get('range', 'day')
    results = youtube_service.get_youtube_data(date_range)


    return jsonify({
        "message": "User registered successfully",
        "data": results
    }), 200