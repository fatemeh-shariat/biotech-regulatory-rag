import os

from dotenv import load_dotenv
from supabase import create_client

# Load variables from the .env file
load_dotenv()

url = os.environ["SUPABASE_URL"]
key = os.environ["SUPABASE_KEY"]

print("URL loaded:", url)
print("Key format OK:", key.startswith("sb_secret_"))

# Create the Supabase client
client = create_client(url, key)
print("Supabase client created successfully")
