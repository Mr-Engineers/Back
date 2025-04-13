import json
import openai
from flask import Blueprint, request, jsonify
from app.services.prompt_service import PromptService
from app.services.auth_service import AuthService
from decorators import token_required

# Initialize services and blueprint
auth_service = AuthService()
prompt_service = PromptService(auth_service.client)
prompt_bp = Blueprint('prompt', __name__)

VALID_PLATFORMS = [
    "Twitter",
    "Youtube",
    "TikTok"
]

VALID_CONTENT_TYPES = [
    "Short video",
    "Long video",
    "Article",
]

SYSTEM_MESSAGE = {
    "role": "system",
    "content": "You are a helpful assistant that only returns JSON."
}

@prompt_bp.route('/api/prompt', methods=['POST'])
@token_required
def get_prompt_content():
    try:
        user_id = request.user["user_id"]
        business_data = prompt_service.get_prompt_data(user_id)

        hashtag_data = request.get_json()
        hashtags = hashtag_data.get("hashtags", []) if hashtag_data else []

        if not isinstance(hashtags, list):
            return jsonify({"error": "Invalid hashtags format. Expected a list."}), 400

        prompt_template = f"""
        You are a content strategist assistant. Based on the following business data, generate a content idea in JSON format with these fields:

        {{
          "title": "...",
          "description": "...",
          "platform": "one of: {', '.join(VALID_PLATFORMS)}",
          "contentType": "one of: {', '.join(VALID_CONTENT_TYPES)}",
          "relevance": numeric between 0 and 100,
          "hashtags": ["#tag1", "#tag2"]
        }}

        Here is the business data:
        {business_data}

        Select the most relevant hashtags:

        Return only the JSON object.
        """

        messages = [SYSTEM_MESSAGE, {"role": "user", "content": prompt_template}]

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages
        )

        content = response.choices[0].message["content"]

        try:
            parsed_json = json.loads(content)
            print(parsed_json)
            response = prompt_service.client.table("contents").insert({
                "title": parsed_json.get("title"),
                "user_id": user_id,
                "description": parsed_json.get("description"),
                "relevance": parsed_json.get("relevance"),
                "platform": parsed_json.get("platform"),
                "type": parsed_json.get("contentType"),
            }).execute()

            content_id = response.data[0]["id"]

            for tag in parsed_json.get("hashtags"):
                prompt_service.client.table("tags").insert({
                    "name": tag,
                    "content_id": content_id,
                }).execute()

            if not response.data or len(response.data) == 0:
                return {"error": "Content creation failed"}

        except json.JSONDecodeError:
            return jsonify({"error": "Invalid JSON returned from OpenAI.", "raw": content}), 500

        return jsonify({"data": parsed_json}), 200

    except Exception as e:
        return jsonify({"error": "An unexpected error occurred.", "details": str(e)}), 500
