from constants import SUPABASE_PROJECT_API_KEY, SUPABASE_PROJECT_URL
from supabase import create_client, Client
import supabase

url = SUPABASE_PROJECT_URL
api_key = SUPABASE_PROJECT_API_KEY
supabase: Client = create_client(url, api_key)

email = input()
password = input()

response = supabase.auth.sign_up(
    {"email": email, "password": password}
)