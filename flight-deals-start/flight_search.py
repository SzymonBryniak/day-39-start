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

    def get_flights(self, *origin):
        responses = []
        def get_responses():
            for r in range(0, len(*origin)):
                print(origin)
                datestr = self.today_str + "," + self.delta_strf

                token = self.get_oAuth_token()

                header = {
                    'Authorization': f'Bearer {token}'
                }
                params = {
                    "origin": f'{origin[0][r][1:]}',
                    "departureDate": rf'{datestr}'
                }
                params_str = urllib.parse.urlencode(params, safe=",")
                endpoint = "https://test.api.amadeus.com/v1/shopping/flight-destinations"
                # ?origin=LON&departureDate=2021-12-01,2021-12-31
                print(params_str)
                response = requests.get(url=endpoint, headers=header,params=params_str)
                response.raise_for_status()
                responses.append(response.json())
            return
        get_responses()
        to_gsheet = {}
        print(responses)
        for country in range(1):
            print(len(responses[0]['data'][0]))
            for i in range(0, len(responses[0]['data'])):
                # print(response.json()['data'][i])
                print(origin[0][0])
                to_gsheet.update({origin[0][0]:[responses[i]['data'][0]['destination'],
                                  responses[i]['data'][0]['departureDate'],
                                  responses[i]['data'][0]['returnDate'],
                                  responses[i]['data'][0]['price']
                                  ]})

        print(to_gsheet)
        return self

    def get_flights_mini(self, origin):
        datestr = self.today_str + "," + self.delta_strf

        token = self.get_oAuth_token()

        header = {
            'Authorization': f'Bearer {token}'
        }
        params = {
            "origin": f'{origin}',
            "departureDate": rf'{datestr}'
        }
        params_str = urllib.parse.urlencode(params, safe=",")
        endpoint = "https://test.api.amadeus.com/v1/shopping/flight-destinations"
        # ?origin=LON&departureDate=2021-12-01,2021-12-31
        response = requests.get(url=endpoint, headers=header, params=params_str)
        response.raise_for_status()
        to_gsheet = {}
        for i in range(0, len(response.json()['data'])):
            # print(response.json()['data'][i])
            to_gsheet.update({origin: [response.json()['data'][i]['destination'],
                                          response.json()['data'][i]['departureDate'],
                                          response.json()['data'][i]['returnDate'],
                                          response.json()['data'][i]['price']
                                          ]})

            print(to_gsheet)

test = FlightSearch()

print(test.get_flights_mini('LON'))
