import os
import json
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
api_key = os.getenv('mailchimp_api_key')
url = f'https://us2.api.mailchimp.com/3.0/campaigns'

# Load existing data from the static file
file_path = 'all_campaigns.json'

# Creates an empty list and set to hold previous campaigns and ids
existing_campaigns = []
existing_ids = set()
latest_time = None

# Checks file exists and loads into the variable defines above
# Extracts the ids of each of the campaigns and stores them in the set
# Create time is used to find the new campaigns 

if os.path.exists(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        existing_campaigns = json.load(f)
        existing_ids = {c['id'] for c in existing_campaigns}
        if existing_campaigns:
            latest_time = max(c['create_time'] for c in existing_campaigns if 'create_time' in c)

# API request parameters, only pulling through campaigns with date after max date in static table
params = {'count': 100}
if latest_time:
    params['since_create_time'] = latest_time

# Fetch new campaigns from Mailchimp
response = requests.get(url, auth=('anystring', api_key), params=params)

if response.status_code != 200:
    print(f"Error {response.status_code}: {response.text}")
    exit()

# Only includes campaigns where id is not alreayd present in the list 
new_campaigns = [
    c for c in response.json().get('campaigns', [])
    if c['id'] not in existing_ids
]

# Append and save if there are new campaigns
if new_campaigns:
    existing_campaigns.extend(new_campaigns)
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(existing_campaigns, f, indent=2)
    print(f"✅ Appended {len(new_campaigns)} new campaigns.")
else:
    print("ℹ️ No new campaigns to append.")

