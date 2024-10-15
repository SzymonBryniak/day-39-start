import requests

class FlightData:
    #This class is responsible for structuring the flight data.
    def __init__(self):
        self.cities = []
        self.oAuth_token = {}
        self.locations_end = "https://test.api.amadeus.com/v1/reference-data/locations"
        self.location_by_id = "https://test.api.amadeus.com/v1/reference-data/locations/idtoenter"
        # self.enter_cities()


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
        print(response.text)
        self.oAuth_token.update(response.json())
        print(self.oAuth_token)

        return self.oAuth_token['access_token']


    def enter_cities(self):
        print("Enter 5 cities")
        while len(self.cities) < 5:
            self.cities.append(input("Please enter a city name: "))



    def get_cities(self):
        # curl
        # 'https://test.api.amadeus.com/v1/shopping/flight-destinations?origin=PAR&maxPrice=200' \
        # - H
        # 'Authorization: Bearer ABCDEFGH12345'
        endpoint = self.locations_end
        token = self.get_oAuth_token()
        print(self.oAuth_token)
        header = {
            'Authorization': f'Bearer {token}'
        }
        params = {
            "subType": "CITY",
            "keyword": "MUNICH"

        }
        response = requests.get(url=endpoint, headers=header, params=params)
        response.raise_for_status()
        print(response.json()["data"][0]['id'])
    pass

cities = FlightData()
cities.get_cities()
