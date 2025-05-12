import requests
from dotenv import load_dotenv
import os
import json

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
    print(data)

    with open('Campaign.json', 'w') as files:
        json.dump(data, files, indent=2)
        
    print('Campaign data extracted')
    
else:
    print(f'Error {response.status_code}:')
    print(response.text)