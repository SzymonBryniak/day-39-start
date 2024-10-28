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
        self.gc = pygsheets.authorize(client_secret='client_secret.json', scopes=['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive'])
        self.oAuth_token = {}
        self.get_oAuth_token()
        self.data = {}

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

    def edit_pygsheet(self,origin, destination, city):
        header = ['FROM', 'CODE', 'TO', 'Departure', 'Return', 'Price']
        try:
            sh2 = self.gc.open('Flights')
            wk1 = sh2[0]
            wk1.update_row(1, header)
        except pygsheets.exceptions.SpreadsheetNotFound:
            sh2 = self.gc.create('Flights')
            sh2 = self.gc.open('Flights')
            wk1 = sh2[0]
            wk1.update_row(1, header)

        wk1 = sh2[0]  # Open first worksheet of spreadsheet
        # Or
        # wks = sh.sheet1 # sheet1 is name of first worksheet
        print(wk1, sh2.url, wk1.get_value('A1'))
        # Append the new row at the end of the worksheet
        print(origin, destination)
        for i in range(0, len(destination)):
            wk1.append_table(values=[[city]+[origin]+destination[i][:-1]+[destination[i][3]['total']]])
        self.data = wk1.get_all_records()


        return self

    def get_worksheet_data(self):
        sh2 = self.gc.open('Flights')
        wk1 = sh2[0]
        worksheet = wk1.get_all_records()

        cities = wk1.get_col(1, include_tailing_empty=False)  # 1 refers to the first column (A)
        departures = wk1.get_col(4, include_tailing_empty=False)
        codes = wk1.get_col(2, include_tailing_empty=False)
        # Get unique values by converting to a set
        unique_cities = list(set(cities))
        unique_departures = list(set(departures))
        unique_codes = list(set(codes))
        return worksheet, unique_cities, unique_departures, unique_codes

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



