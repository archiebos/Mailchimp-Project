# 1.        Import libraries requests and JSON

import requests
from dotenv import load_dotenv
import os
import json
import csv

# 2.         Define variables: URL,
# 3.        Define API keys in a virtual environment so key information isn’t available on GitHub

load_dotenv()

api_key = os.getenv('mailchimp_api_key')  
url = f'https://us2.api.mailchimp.com/3.0/campaigns'

# Make request with Basic Auth
response = requests.get(url, auth=('', api_key))


# 4.        Get response
# 5.        Write an if statement that returns the data or an error message

if response.status_code == 200:
    print('good job')
    
    data = response.json()
    campaigns = data.get('campaigns',[])
    
    #Trying to create a CSV file
    
    csv_file = 'campaigns.csv'
    
    with open(csv_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        
        
        writer.writerow(['ID', 'Subject', 'Status', 'Emails Sent', 'Create Time'])

        # Write campaign rows
        for campaign in campaigns:
            writer.writerow([
                campaign.get('id'),
                campaign.get('subject_line'),
                campaign.get('status'),
                campaign.get('emails_sent'),
                campaign.get('create_time'),
            ])

    print(f'Campaign data saved to {csv_file}')
    

    # with open('Campaign.json', 'w') as files:
    #     json.dump(data, files, indent=2)
        
    print('Campaign data extracted')
    
else:
    print(f'Error {response.status_code}:')
    print(response.text)



# 6.        Export as a zip using with, open

# 7.        Add requirements.txt

# 8.        Move that to AWS