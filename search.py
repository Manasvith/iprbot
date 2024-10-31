from constants import SUPABASE_PROJECT_API_KEY, SUPABASE_PROJECT_URL
from supabase import create_client, Client
import supabase

url = SUPABASE_PROJECT_URL
api_key = SUPABASE_PROJECT_API_KEY
supabase: Client = create_client(url, api_key)

history = supabase.table("first_prompts_per_date").select("*").execute()
print(history.count)