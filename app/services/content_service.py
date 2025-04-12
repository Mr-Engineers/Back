from supabase import create_client, Client
import os

class ContentService:
    def __init__(self):
        self.url = os.getenv("SUPABASE_URL")
        self.key = os.getenv("SUPABASE_KEY")
        self.client: Client = create_client(self.url, self.key)

    def get_content(self, user_id: str):
        response = self.client.table("contents") \
            .select("*, tags(*)") \
            .eq("user_id", user_id) \
            .execute()

        if not response.data:
            return []

        return response.data

    def add_content(self, user_id: str, data: dict):

        response = self.client.table("contents").insert({
            "title": data.get("title"),
            "user_id": user_id,
            "description": data.get("description"),
            "relevance": data.get("relevance"),
            "platform": data.get("platform"),
            "type": data.get("type"),
        }).execute()

        if not response.data or len(response.data) == 0:
            return {"error": "Content creation failed"}

        content_id = response.data[0]["id"]

        for tag in data.get("tags"):
            self.client.table("tags").insert({
                "name": tag,
                "content_id": content_id,
            }).execute()

        return {"message": "User updated successfully"}