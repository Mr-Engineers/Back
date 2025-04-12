import json
import openai
from flask import Blueprint, request, jsonify
from app.services.prompt_service import PromptService
from decorators import token_required
from app.services.auth_service import AuthService

auth_service = AuthService()
prompt_service = PromptService(auth_service.client)
prompt_bp = Blueprint('prompt', __name__)


@prompt_bp.route('/api/prompt', methods=['GET'])
@token_required
def get_data():
    prompt_input = prompt_service.get_prompt_data(request.user["user_id"])
    # hashtags = request.get_json()

    prompt = f"""
You are a content strategist assistant. Based on the following business data, generate a content idea in JSON format with these fields:

{{
  "title": "...",
  "description": "...",
  "platform": "one of: twitter, youtube, tiktok",
  "contentType": "one of: twitter article, youtube long video, tik tok short",
  "relevance": numeric between 0 and 100,
  "hashtags": ["#tag1", "#tag2"]
}}

Here is the business data:
{prompt_input}

Return only the JSON object.
"""

    messages = [
        {"role": "system", "content": "You are a helpful assistant that only returns JSON."},
        {"role": "user", "content": prompt}
    ]

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )

    # Get raw string content from OpenAI
    content = response.choices[0].message["content"]

    try:
        # Parse the string to a JSON object (Python dict)
        parsed = json.loads(content)
    except json.JSONDecodeError:
        return jsonify({"error": "Invalid JSON returned from OpenAI.", "raw": content}), 500

    return jsonify({
        "data": parsed,
    }), 200
