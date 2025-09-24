import json
import pandas as pd
from datetime import datetime
from supabase import create_client, Client

#Load JSON from file
with open('data/raw_blob.txt', 'r') as f:
    data = json.load(f)

#Convert to DataFrame
df = pd.DataFrame(data)
now = datetime.utcnow().isoformat()
df['updated_at'] = now

print(df.head())

#Supa base logic
url = "https://rgajvixmvdtoeuojjiaa.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJnYWp2aXhtdmR0b2V1b2pqaWFhIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTU3MTUyNTMsImV4cCI6MjA3MTI5MTI1M30.mFVi4YyBG1epPeq5nQlWB8ODjl0RGfg1qRppUQGooI8"
supabase: Client = create_client(url, key)

table_name = "nfl_rushing_2024_2025"

#Update and insert
for _, row in df.iterrows():
    record = row.to_dict()
    supabase.table(table_name).upsert(record).execute()

print("Upsert complete.")
