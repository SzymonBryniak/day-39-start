from re import search
from data_manager import DataManager
import notification_manager
import flight_data
from flight_search import FlightSearch

 # I am skipping this day for now because my tokens don't work anymore.
 # This is the first day I will leave finishing for later.
def main_app():
    # enter cities
    cities = flight_data.FlightData()
    cities.enter_cities()
        # append cities
    for i in range(1):
        cities.code.append(cities.get_cities(i))
        # pass entered cities list to flight search

    search = FlightSearch()
    to_gsheet = search.get_flights(cities.code)

        # populate gsheet
    # print(to_gsheet)
    gsheet = DataManager()

    # gsheet.edit_pygsheet(cities.cities, cities.code)
    for key, value in to_gsheet.items():
        gsheet.edit_pygsheet(key,value, cities.cities[0])



    # update gsheet with better price s

def test_app():

    search = FlightSearch()
    search.flight_offers_search('PAR', 'MAD', '2024-10-30')

def update_prices():
    search = FlightSearch()
    gsheet = DataManager()
    worksheet, cities, departures, codes = gsheet.get_worksheet_data()
    print(f'worksheet data: {worksheet}')
    print(f'cities: {cities}')
    print(f'departures: {sorted(departures)}')
    print(f'code {codes}')
    price_update = search.get_flights(codes[-1])
    print(price_update)


test_app()


# import aiohttp
# import asyncio
# import requests
#
# endpoint = "https://test.api.amadeus.com/v1/security/oauth2/token"
# header = {
#     "Content-Type": "application/x-www-form-urlencoded"
# }
# data = {
#     "grant_type":"client_credentials",
#     "client_id":"UXGJDIsRiO7S1HG1vjZDejxwXXLkzXSk",
#     "client_secret":"Z1VZxFkX9CpMAWz6"
# }
# response = requests.post(url=endpoint, headers=header, data=data)
# response.raise_for_status()
# print(response.text)
# access_token = response.json()['access_token']
#
# async def main():
#     headers = {'Authorization': 'Bearer' + ' ' + access_token}
#     flight_search_endpoint = 'https://test.api.amadeus.com/v2/reference-data/locations'
#     parameters = {"airlineCode": 'BA'}
#
#     async with aiohttp.ClientSession() as session:
#
#         for number in range(20):
#             async with session.get(flight_search_endpoint,
#                             params=parameters,
#                             headers=headers) as resp:
#                 flights = await resp.json()
#                 print(flights)
#
# asyncio.run(main())


# Program Requirements
# Use the Flight Search and Sheety API to populate your own copy of the Google Sheet with International Air Transport Association (IATA) codes for each city. Most of the cities in the sheet include multiple airports, you want the city code (not the airport code see here).
#
# Use the Flight Search API to check for the cheapest flights from tomorrow to 6 months later for all the cities in the Google Sheet.
#
# If the price is lower than the lowest price listed in the Google Sheet then send an SMS (or WhatsApp Message) to your own number using the Twilio API.
#
# The SMS should include the departure airport IATA code, destination airport IATA code, flight price and flight dates. e.g.
#
# Avoid hitting your rate limit on your trial accounts by not using too many destination airports in your google Sheet (use 5 or at most 10)
#
# Also, the test Amadeus test API does not include all airports. You may not be able to retrieve prices for many routes flights. Try and stick to popular airports while practicing.


