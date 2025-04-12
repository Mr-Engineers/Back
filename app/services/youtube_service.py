from supabase import create_client, Client
import os
from pymongo import MongoClient
from datetime import datetime, timedelta

class YoutubeService:
    def __init__(self):
        self.uri = os.getenv("MONGO_URI")

    def get_youtube_data(self, date_range):
        client = MongoClient(self.uri)
        db = client["Hacknarok"]
        collection = db["Youtube"]

        now = datetime.now()

        if date_range == "week":
            start_date = now - timedelta(weeks=1)
        elif date_range == "month":
            start_date = now - timedelta(days=30)
        else:
            start_date = now - timedelta(days=1)

        query = {
            "date": {"$gte": start_date}
        }

        documents = list(collection.find(query, {'_id': 0}))

        return documents