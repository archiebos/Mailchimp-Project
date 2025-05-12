# 1.        Import libraries requests and JSON

import requests
from dotenv import load_dotenv
import os
import json


load_dotenv()

api_key = os.getenv('mailchimp_api_key')  

url = f'https://us2.api.mailchimp.com/3.0/campaigns'

# Make request with Basic Auth
response = requests.get(url, auth=('', api_key))



if response.status_code == 200:
    print('good job')
    
    data = response.json()
    print(data)


# 3.        Define API keys in a virtual environment so key information isn’t available on GitHub

# 4.        Get response

# 5.        Write an if statement that returns the data or an error message

# 6.        Export as a zip using with, open

# 7.        Add requirements.txt

# 8.        Move that to AWS