from flask import Blueprint, request, jsonify
from app.services.tiktok_service import TiktokService
from decorators import token_required

tiktok_bp = Blueprint('tiktok', __name__)
tiktok_service = TiktokService()


@tiktok_bp.route('/api/tiktok', methods=['GET'])
@token_required
def get_data():
    date_range = request.args.get('range', 'day')
    results = tiktok_service.get_tiktok_data(date_range)

    return jsonify({
        "message": "Tiktok data acquired",
        "data": results
    }), 200
