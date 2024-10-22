import requests
from datetime import datetime, timedelta
import urllib.parse
from dateutil.utils import today


class FlightSearch:
    #This class is responsible for talking to the Flight Search API.
    def __init__(self):
       self.oAuth_token = {}
       today = datetime.today() + timedelta(days=1)
       self.today_str = today.strftime("%Y-%m-%d")
       delta = datetime.now() + timedelta(days=5)
       self.delta_strf = str(delta.strftime("%Y-%m-%d"))
       self.time = datetime.now().strftime("%H:%M:%S")
       self.to_gsheet = {}
    pass


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

        return self.oAuth_token['access_token']

    def get_flights(self, origin):
        for o in range(0, len(origin)):
            print(origin[o][1:])
            datestr = self.today_str + "," + self.delta_strf

            token = self.get_oAuth_token()

            header = {
                'Authorization': f'Bearer {token}'
            }
            params = {
                "origin": f'{origin[o][1:]}',
                "departureDate": rf'{datestr}'
            }
            params_str = urllib.parse.urlencode(params, safe=",")
            endpoint = "https://test.api.amadeus.com/v1/shopping/flight-destinations"
            # ?origin=LON&departureDate=2021-12-01,2021-12-31
            response = requests.get(url=endpoint, headers=header, params=params_str)
            response.raise_for_status()
            to_gsheet = {}
            to_gsheet.update({origin[0]:[]})
            for i in range(0, len(response.json()['data'])):
                # print(response.json()['data'][i])
                to_gsheet[f'{origin[0]}'].append([[response.json()['data'][i]['destination'],
                                          response.json()['data'][i]['departureDate'],
                                          response.json()['data'][i]['returnDate'],
                                          response.json()['data'][i]['price']
                                          ]])


            return to_gsheet




test = FlightSearch()

# print(test.get_flights_mini('LON'))
    # to handle the below exception. I will continue and ask to enter a different city.
    # requests.exceptions.HTTPError: 429 Client Error: Too Many Requests for url:
