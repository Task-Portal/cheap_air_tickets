import requests
import os
from dotenv import load_dotenv
load_dotenv()


def get_Token():

    client_id = os.environ.get('CLIENT_ID')
    client_secret = os.environ.get('CLIENT_SECRET')

    token_url = 'https://test.api.amadeus.com/v1/security/oauth2/token'

    data = {
        'grant_type': 'client_credentials',
    }

    response = requests.post(token_url, data=data,
                             auth=(client_id, client_secret))

    data = response.json()
    access_token = data['access_token']
    return access_token


def get_IATA_code(town):

    endpoint = 'https://test.api.amadeus.com/v1/reference-data/locations'

    params = {
        'subType': 'CITY',
        'keyword': town,
    }

    token = get_Token()
    headers = {
        'Authorization': f'Bearer {token}'
    }

    response = requests.get(endpoint, params=params, headers=headers)

    data = response.json()
    if 'data' in data and len(data['data']) > 0:
        iata_code = data['data'][0]['iataCode']
        return iata_code
    else:
        return None
