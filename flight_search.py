
from pprint import pprint
from flight_deal import FlightDeal
from dotenv import load_dotenv
import requests
import os

load_dotenv()
class FlightSearch:
    def __init__(self):
        self.tequila_endpoint = "https://api.tequila.kiwi.com/v2/search"
        self.api_key = os.environ.get('API_KEY_TEQUILA_KIWI')
        



    def search_flights(self, fly_to_code,fly_from_code, price, from_date, to_date):
        params={
            "fly_from":fly_from_code,
            "fly_to":fly_to_code,
            "dateFrom" : from_date,
            "dateTo":to_date

        }
        headers = {
            "apikey":self.api_key
        }
        response= requests.get(self.tequila_endpoint,params=params, headers=headers)
        response.raise_for_status()
        

        trip = []
        
        for i in response.json()['data']:
            if float(i["price"])<=float(price):                
                trip.append(FlightDeal(i))
        
        return trip
















