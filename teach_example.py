import requests
from bs4 import BeautifulSoup
import openai
from openai import OpenAI
import json
import os
#scrape info from website
scrap_url = 'https://www.statmuse.com/nfl/ask/nfl-rushing-leaders-2024-to-2025'  # Replace with the new website URL
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36'
}

# Get HTML for troubleshooting
html_response = requests.get(scrap_url, headers=headers)
soup = BeautifulSoup(html_response.text, "html.parser")
table = soup.find("table")  
if table:
    rows = table.find_all("tr")
    extracted_data = []

    for i, row in enumerate(rows[1:]):
        cols = row.find_all("td")
        col_texts = [col.text.strip() for col in cols]
        if len(col_texts) > 8:
            name = col_texts[2]  #Names and abreviations
            rush_yds = col_texts[3]  #Rushing yards
            rush_td = col_texts[8]  #Rushing touchdowns
            #append data to structured list so long as all fields are non-empty
            if name and rush_yds and rush_td:
                extracted_data.append({
                    "Name": name,
                    "Rushing Yards": rush_yds,
                    "Rushing Touchdowns": rush_td
                })
else:
    extracted_data = "No data found"

print("Extracted Data:")
print(extracted_data)

#save the data as a json file
with open('data/raw_blob.txt', 'w') as f:
    json.dump(extracted_data, f, indent=2)
#Gpt api call and instructions for LLM
# Initialize the GPT API client
endpoint = os.getenv("GPT_API_ENDPOINT", "<your-endpoint-here>")
api_key = os.getenv("GPT_API_KEY", "<your-api-key-here>")
deployment_name = os.getenv("GPT_DEPLOYMENT", "gpt-4o")
client = OpenAI(
    base_url=endpoint,
    api_key=api_key
)

response = client.chat.completions.create(
    model=deployment_name,
    messages=[
        {
            "role": "system",
            "content": "You are a helpful assistant. Clean and format the following preprocessed data into a JSON output. Extract fields such as Name, Rushing Yards, and Rushing Touchdowns, and ensure the JSON is well-structured."
        },
        {
            "role": "user",
            "content": f"Here is the preprocessed data: {extracted_data}"
        }
    ],
    temperature=0.1
)
print("GPT API Response:")
print(response.choices[0].message.content)
# NOTE: Create a .env file with the following (do not commit it):
# GPT_API_KEY=your_key_here
# GPT_API_ENDPOINT=your_endpoint_here
# GPT_DEPLOYMENT=gpt-4o

