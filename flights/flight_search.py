import os
import requests

SERPAPI_ENDPOINT = "https://serpapi.com/search"

class FlightSearch:
    def __init__(self):
        self._api_key = os.environ["SERPAPI_API_KEY"]

    def check_flights(self, origin_city_code, destination_city_code, from_time):
        query = {
            "engine": "google_flights",
            "departure_id": origin_city_code,
            "arrival_id": destination_city_code,
            "outbound_date": from_time.strftime("%Y-%m-%d"), # Optional
            "type": "2", # One Way
            "adults": "1",
            "currency": "INR",
            "api_key": self._api_key,
            "stops": "1", # Non Stop
            "gl": "in", # Country India
            "hl": "en", # Language English
            "outbound_times": "9,21", # Departure between 9.00 AM & 10.00 PM
        }

        response = requests.get(url=SERPAPI_ENDPOINT, params=query)

        if response.status_code != 200:
            print(f"check_flights() response code: {response.status_code}")
            print(f"check_flights() response code: {response.text}")
            return None

        data = response.json()
        if "error" in data:
            print(f"API error: {data['error']}")
            return None
        return data
