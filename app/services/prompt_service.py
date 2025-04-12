from supabase import Client


class PromptService:
    def __init__(self, client: Client):
        self.client = client

    def get_prompt_data(self, user_id: str):
        response = self.client.table("business_profiles").select("*").eq("user_id", user_id).execute()
        return response.data
