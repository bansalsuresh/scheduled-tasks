from datetime import datetime, timedelta
from pathlib import Path
from pprint import pprint

import pandas as pd

from flights.flight_data import find_cheapest_flight
from flights.flight_search import FlightSearch

FILE_PATH = Path(__file__).with_name("flights.xlsx")

def has_value(value):
    return pd.notna(value) and str(value).strip() != ""

def get_flight_dates(destination, default_date):
    from_date = destination.get("From")
    to_date = destination.get("To")

    if not has_value(from_date) or not has_value(to_date):
        return [default_date]

    start_date = pd.to_datetime(from_date).to_pydatetime()
    end_date = pd.to_datetime(to_date).to_pydatetime()

    flight_dates = []
    current_date = start_date
    while current_date <= end_date:
        flight_dates.append(current_date)
        current_date += timedelta(days=1)

    return flight_dates


def get_cheapest_flight_for_dates(destination, flight_search, default_date, flight_data):
    cheapest_flight = None

    for flight_date in get_flight_dates(destination, default_date):
        flight_data += f"Getting flights {destination['Start']} - {destination['End']} on {flight_date.strftime('%Y-%m-%d')}\n"
        flights = flight_search.check_flights(
            destination["Start"],
            destination["End"],
            from_time=flight_date,
        )
        flight = find_cheapest_flight(flights)
        flight_data += f"{str(flight)}\n"

        if flight.price == "N/A":
            continue

        if cheapest_flight is None or flight.price < cheapest_flight.price:
            cheapest_flight = flight

    return cheapest_flight, flight_data

def run_flight_alerts():
    flight_data: str
    sheet_data = pd.read_excel(FILE_PATH).to_dict("records")
    flight_search = FlightSearch()
    default_flight_date = datetime.now() + timedelta(days=10)

    flight_data = ""
    for destination in sheet_data:
        cheapest_flight, flight_data = get_cheapest_flight_for_dates(destination, flight_search, default_flight_date, flight_data)

        if cheapest_flight is not None and cheapest_flight.price < destination["Price"]:
            flight_data += f"Price Alert: {str(cheapest_flight)}!\n"

    return flight_data
