from supabase import Client


class PromptService:
    def __init__(self, client: Client):
        self.client = client

    def get_prompt_data(self, user_id: str):
        # Fetch data from Supabase
        industry_result = self.client.table("business_profiles").select("industry").eq("user_id", user_id).execute()
        description_result = self.client.table("business_profiles").select("business_description").eq("user_id", user_id).execute()
        goals_result = self.client.table("content_goals").select("goal_id").eq("user_id", user_id).execute()

        # Extract values
        industry = industry_result.data[0]["industry"] if industry_result.data else None
        business_description = description_result.data[0]["business_description"] if description_result.data else None
        content_goals = [item["goal_id"] for item in goals_result.data] if goals_result.data else []

        # Return a flat and clear structure
        return {
            "industry": industry,
            "business_description": business_description,
            "content_goals": content_goals
        }
