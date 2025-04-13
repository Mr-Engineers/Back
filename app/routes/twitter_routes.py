from flask import Blueprint, request, jsonify
from app.services.twitter_service import TwitterService
from decorators import token_required


twitter_bp = Blueprint('twitter', __name__)
twitter_service = TwitterService()

@twitter_bp.route('/api/twitter', methods=['GET'])
@token_required
def get_data():
    date_range = request.args.get('range', 'day')
    results = twitter_service.get_twitter_data(date_range)


    return jsonify({
        "message": "Twitter data acquired",
        "data": results
    }), 200