# 1. Import libraries
import requests
from dotenv import load_dotenv
import os
import json

# 2. Load API key from .env file
load_dotenv()
api_key = os.getenv('mailchimp_api_key')

# 3. Set Mailchimp API endpoint
url = 'https://us2.api.mailchimp.com/3.0/campaigns'

# 4. Pagination setup
count = 50
offset = 0
all_campaigns = []

# 5. Loop through pages
while True:
    params = {
        'count': count,
        'offset': offset
    }

    # 6. Make authenticated request
    response = requests.get(url, auth=('anystring', api_key), params=params)

    # 7. Check response
    if response.status_code != 200:
        print(f"Error {response.status_code}: {response.text}")
        break

    data = response.json()
    campaigns = data.get('campaigns', [])

    if not campaigns:
        break

    all_campaigns.extend(campaigns)
    offset += count

    print(f"Fetched {len(campaigns)} campaigns, total so far: {len(all_campaigns)}")

# 8. Save to JSON file
json_file = 'all_campaigns.json'
with open(json_file, 'w', encoding='utf-8') as f:
    json.dump(all_campaigns, f, indent=2)

print(f"Saved {len(all_campaigns)} campaigns to {json_file}")
