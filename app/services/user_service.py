from supabase import create_client, Client
import os

class UserService:
    def __init__(self):
        self.url = os.getenv("SUPABASE_URL")
        self.key = os.getenv("SUPABASE_KEY")
        self.client: Client = create_client(self.url, self.key)

    def get_user_by_email(self, user_id: str):
        response = self.client.table("profiles").select("*").eq("id", user_id).execute()
        business_profiles = self.client.table("business_profiles").select("*").eq("user_id", user_id).execute()
        content_goals = self.client.table("content_goals").select("goal_id").eq("user_id", user_id).execute()
        all_goals = []
        for goal in content_goals.data:
            all_goals.append(goal.get("goal_id"))
        if business_profiles.data and len(response.data) > 0:
            return {
                "name": response.data[0].get("name"),
                "email": response.data[0].get("email"),
                "businessName": business_profiles.data[0].get("business_name"),
                "business_type" : business_profiles.data[0].get("business_type"),
                "industry": business_profiles.data[0].get("industry"),
                "businessDescription": business_profiles.data[0].get("business_description"),
                "contentGoals": all_goals,

            }
        else:
            return None
