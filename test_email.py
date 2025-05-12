import requests
from dotenv import load_dotenv
import os
import json

# Load environment variables (API key)
load_dotenv()

# Retrieve Mailchimp API key
api_key = os.getenv('mailchimp_api_key')

# Extract datacenter from the API key (e.g., 'us2')
dc = api_key.split('-')[-1]

# Load campaign IDs from JSON file
with open('all_campaigns.json', 'r', encoding='utf-8') as f:
    campaigns = json.load(f)

# Extract all campaign IDs
campaign_ids = [campaign['id'] for campaign in campaigns if 'id' in campaign]

print(f"Found {len(campaign_ids)} campaigns.")

# File to save email activity data
activity_file = 'email_activity.json'

# Load existing email activity data if available
existing_activity = []
seen = set()  # To keep track of already fetched records (campaign_id, email_id)

if os.path.exists(activity_file):
    with open(activity_file, 'r', encoding='utf-8') as f:
        existing_activity = json.load(f)
        seen = {(a['campaign_id'], a['email_id']) for a in existing_activity if 'campaign_id' in a and 'email_id' in a}

# List to collect new activity records
new_activity = []

# Loop through each campaign ID to fetch email activity
for campaign_id in campaign_ids:
    count = 1000  # Number of records per request
    offset = 0   # Starting point for pagination

    print(f"\nFetching email activity for campaign {campaign_id}...")

    while True:
        # Construct the API request URL with pagination
        url = f'https://{dc}.api.mailchimp.com/3.0/reports/{campaign_id}/email-activity?count={count}&offset={offset}'

        # Send GET request to the Mailchimp API
        response = requests.get(url, auth=('', api_key))

        # Check for successful response
        if response.status_code != 200:
            print(f"❌ Error fetching activity for campaign {campaign_id}: {response.status_code}")
            break

        # Get email activity data from the response
        data = response.json().get('emails', [])

        # If no more data is returned, exit the loop
        if not data:
            break

        # Process each email activity entry
        for entry in data:
            email_id = entry.get('email_id')
            if not email_id:
                continue

            unique_key = (campaign_id, email_id)

            # Avoid duplicates using a set of (campaign_id, email_id)
            if unique_key not in seen:
                entry['campaign_id'] = campaign_id
                new_activity.append(entry)
                seen.add(unique_key)

        # Update offset to fetch the next page of results
        offset += count
        print(f"Fetched {len(data)} records for campaign {campaign_id}, total so far: {offset}")

# Combine existing and new activity data
if new_activity:
    combined_activity = existing_activity + new_activity

    # Save combined activity data into JSON file
    with open(activity_file, 'w', encoding='utf-8') as f:
        json.dump(combined_activity, f, indent=2)

    print(f"\nAppended {len(new_activity)} new records. Total records: {len(combined_activity)}")
else:
    print("\nNo new activity found.")
