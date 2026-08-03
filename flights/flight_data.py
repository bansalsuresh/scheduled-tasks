from pprint import pprint


class FlightData:

    def __init__(self, price, origin_airport, destination_airport, out_date, out_time, airline=None, flight_number=None):
        self.price = price
        self.origin_airport = origin_airport
        self.destination_airport = destination_airport
        self.out_date = out_date
        self.out_time = out_time
        self.airline = airline
        self.flight_number = flight_number

    def __str__(self):
        return object_to_string(self)

def object_to_string(obj):
    return (
        f"Origin: {obj.origin_airport}, "
        f"Destination: {obj.destination_airport}, "
        f"Date: {obj.out_date}; {obj.out_time}, "
        f"Airline: {obj.airline}; {obj.flight_number}, "
        f"Price: {obj.price}"
    )

def find_cheapest_flight(data):
    # Handle empty data if no flight data is returned
    if data is None or (not data.get("best_flights") and not data.get("other_flights")):
        print("No flight data")
        return FlightData("N/A", "N/A", "N/A", "N/A", out_time="N/A", airline="N/A", flight_number="N/A")

    # Combine best_flights and other_flights into one list
    all_flights = data.get("best_flights", []) + data.get("other_flights", [])

    # Data from the first flight in the list
    first_flight = all_flights[0]
    lowest_price = first_flight["price"]
    origin = first_flight["flights"][0]["departure_airport"]["id"]
    airline = first_flight["flights"][0]["airline"]
    flight_number = first_flight["flights"][0]["flight_number"]
    destination = first_flight["flights"][-1]["arrival_airport"]["id"]
    out_date = first_flight["flights"][0]["departure_airport"]["time"].split(" ")[0]
    out_time = first_flight["flights"][0]["departure_airport"]["time"].split(" ")[1]

    # Initialize FlightData with the first flight for comparison
    cheapest_flight = FlightData(lowest_price, origin, destination, out_date, out_time, airline, flight_number)

    for flight in all_flights:
        # Exception handling - json has data but flight is missing 'price'. Skip.
        try:
            price = flight["price"]
        except KeyError:
            # print("--- No price available for flight. ---")
            continue
        if price < lowest_price:
            lowest_price = price
            cheapest_flight.price = price
            cheapest_flight.airline = first_flight["flights"][0]["airline"]
            cheapest_flight.flight_number = first_flight["flights"][0]["flight_number"]
            cheapest_flight.out_time = first_flight["flights"][0]["departure_airport"]["time"].split(" ")[1]

    return cheapest_flight
