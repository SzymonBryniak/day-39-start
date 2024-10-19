import pygsheets
import requests
from datetime import datetime
import json

from aiohttp.client_exceptions import cert_errors
from gspread import SpreadsheetNotFound


# curl "https://test.api.amadeus.com/v1/security/oauth2/token" \
#      -H "Content-Type: application/x-www-form-urlencoded" \
#      -d "grant_type=client_credentials&client_id={client_id}&client_secret={client_secret}"

class DataManager:

    def __init__(self):

        self.today = datetime.now().strftime("%d/%m/%Y")
        self.time = datetime.now().strftime("%H:%M:%S")
        self.oAuth_token = {}

    # This file will need to use the DataManager,FlightSearch, FlightData, NotificationManager classes to achieve the program requirements.
    # APIs used
    # I will use pygsheet instead of sheety
    # Google Sheet Data Management - https://sheety.co/
    #
    # Amadeus Flight Search API (Free Signup, Credit Card not required) - https://developers.amadeus.com/
    #
    # Amadeus Flight Offer Docs - https://developers.amadeus.com/self-service/category/flights/api-doc/flight-offers-search/api-reference
    #
    # Amadeus How to work with API keys and tokens guide - https://developers.amadeus.com/get-started/get-started-with-self-service-apis-335
    #
    # Amadeus Search for Airport Codes by City name - https://developers.amadeus.com/self-service/category/destination-experiences/api-doc/city-search/api-reference
    # I will use smtplib with mime instead of twilio.
    # Twilio Messaging (SMS or WhatsApp) API - https://www.twilio.com/docs/messaging/quickstart/python
    def get_oAuth_token(self):
        endpoint = "https://test.api.amadeus.com/v1/security/oauth2/token"
        header = {
            "Content-Type": "application/x-www-form-urlencoded"
        }
        data = {
            "grant_type":"client_credentials",
            "client_id":"UXGJDIsRiO7S1HG1vjZDejxwXXLkzXSk",
            "client_secret":"Z1VZxFkX9CpMAWz6"
        }

        response = requests.post(url=endpoint, headers=header, data=data)
        response.raise_for_status()
        self.oAuth_token.update(response.json())
        print(self.oAuth_token)

        return self.oAuth_token['access_token']

    def edit_pygsheet(self, city, code):
        gc = pygsheets.authorize(client_secret='client_secret.json')
        headers = ['CITY', 'CODE', 'AIRPORT', 'PRICE', 'TO']
        try:
            sh2 = gc.open('Flights')
        except SpreadsheetNotFound:
            sh2 = gc.create('Flights')
            wk1 = sh2[0]
            wk1.update_values('A1:E1', [headers])

        wk1 = sh2[0]  # Open first worksheet of spreadsheet
        # Or
        # wks = sh.sheet1 # sheet1 is name of first worksheet
        print(wk1, sh2.url, wk1.get_value('A1'))
        # Append the new row at the end of the worksheet

        for i in range(2, len(city)+2):
            wk1.append_table(values=[city[i-2], code[i-2]])


        return self

    def get_destinations_test(self):
        # curl
        # 'https://test.api.amadeus.com/v1/shopping/flight-destinations?origin=PAR&maxPrice=200' \
        # - H
        # 'Authorization: Bearer ABCDEFGH12345'
        endpoint = 'https://test.api.amadeus.com/v1/shopping/flight-destinations'
        token = self.get_oAuth_token()
        print(self.oAuth_token)
        params = {
            "origin": "PAR",
            "maxPrice": "200"
        }
        header = {
            'Authorization': f'Bearer {token}'
        }
        response = requests.get(url=endpoint, headers=header, params=params)
        response.raise_for_status()
        print(response.text)



