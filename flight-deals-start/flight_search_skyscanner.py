import requests


def flights_cheapest_one_way():
    url = "https://sky-scanner3.p.rapidapi.com/flights/cheapest-one-way"

    querystring = {"departDate":"2024-11-11",
                    "fromEntityId":"LON",
                    "toEntityId":"PAR"}

    headers = {
        "x-rapidapi-key": "d2f1f3fb91mshb13a1ad30f8cf25p17c760jsne6ec4a660e4f",
        "x-rapidapi-host": "sky-scanner3.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    print(response.json())


def airports():
    url = "https://sky-scanner3.p.rapidapi.com/flights/airports"

    headers = {
        "x-rapidapi-key": "d2f1f3fb91mshb13a1ad30f8cf25p17c760jsne6ec4a660e4f",
        "x-rapidapi-host": "sky-scanner3.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers)

    print(response.json())


def search_one_way():
    import requests

    url = "https://sky-scanner3.p.rapidapi.com/flights/search-one-way"

    querystring = {"fromEntityId": "PARI", "cabinClass": "economy"}

    headers = {
        "x-rapidapi-key": "d2f1f3fb91mshb13a1ad30f8cf25p17c760jsne6ec4a660e4f",
        "x-rapidapi-host": "sky-scanner3.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    print(response.json())

search_one_way()
