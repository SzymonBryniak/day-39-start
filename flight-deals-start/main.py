from data_manager import DataManager
import notification_manager
import flight_data
import flight_search


cities = flight_data.FlightData()
for i in range(2):
    cities.code.append(cities.get_cities(i))

gsheet = DataManager()
gsheet.edit_pygsheet(cities.cities, cities.code)


#This file will need to use the DataManager,FlightSearch, FlightData, NotificationManager classes to achieve the program requirements.
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

