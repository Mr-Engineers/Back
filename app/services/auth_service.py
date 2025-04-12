from supabase import create_client, Client
import os

class AuthService:
    def __init__(self):
        self.url = os.getenv("SUPABASE_URL")
        self.key = os.getenv("SUPABASE_KEY")
        self.client: Client = create_client(self.url, self.key)

    def register_user(self, email: str, password: str):
        result = self.client.auth.sign_up({"email": email, "password": password})
        return result

    def login_user(self, email: str, password: str):
        result = self.client.auth.sign_in_with_password({"email": email, "password": password})
        return result

