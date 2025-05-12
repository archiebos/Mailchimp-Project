import requests
import json
from dotenv import load_dotenv
import os
from datetime import datetime
from dateutil import parser as date_parser

# Load environment variables
load_dotenv()
api_key = os.getenv('mailchimp_api_key')

# 1. Load existing email activity to find the latest timestamp
try:
    with open('email_activity.json', 'r', encoding='utf-8') as f:
        existing_activity = json.load(f)
except FileNotFoundError:
    existing_activity = []

# 2. Get the latest timestamp from the static file
if existing_activity:
    timestamps = [
        date_parser.parse(entry.get('timestamp', entry.get('timestamp_sent', '')))
        for entry in existing_activity
        if entry.get('timestamp') or entry.get('timestamp_sent')
    ]
    max_timestamp = max(timestamps).isoformat()
else:
    max_timestamp = None

print(f"Latest timestamp from existing data: {max_timestamp}")

# 3. Load new campaigns from new_campaigns.json
with open('new_campaigns.json', 'r', encoding='utf-8') as f:
    new_campaigns = json.load(f)

campaign_ids = [c['id'] for c in new_campaigns if 'id' in c]

# 4. Fetch new email activity only after max_timestamp
new_activity = []

for campaign_id in campaign_ids:
    print(f"Fetching activity for campaign ID {campaign_id}...")

    url = f'https://us2.api.mailchimp.com/3.0/campaigns/{campaign_id}/activity'
    params = {'since': max_timestamp} if max_timestamp else {}

    response = requests.get(url, auth=('', api_key), params=params)

    if response.status_code == 200:
        data = response.json()
        activity = data.get('emails', [])
        if activity:
            new_activity.extend(activity)
            print(f" - Fetched {len(activity)} new activities.")
        else:
            print(" - No new activity found.")
    else:
        print(f" - Error {response.status_code} for campaign {campaign_id}: {response.text}")

# 5. Append new activity to the existing and save
combined_activity = existing_activity + new_activity

with open('email_activity.json', 'w', encoding='utf-8') as f:
    json.dump(combined_activity, f, indent=2)

print(f"Updated email_activity.json with {len(new_activity)} new records. Total: {len(combined_activity)}.")
