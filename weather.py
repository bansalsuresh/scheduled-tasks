import os
import requests
from send_email import EmailFunctions

WEATHER_API_KEY = os.environ.get("WEATHER_API_KEY")
WEATHER_URL = "https://api.openweathermap.org/data/2.5/forecast"
LONGITUDE = 73.772134
LATITUDE = 18.567105
TO_EMAIL = "bansalsuresh75@yahoo.com"

weather_params = {
    "lat": LATITUDE,
    "lon": LONGITUDE,
    "appid": WEATHER_API_KEY,
    "units": "metric",
    "cnt": 4,
}

def get_weather_data():
    response = requests.get(WEATHER_URL, params=weather_params)
    response.raise_for_status()
    return response.json()

def print_weather_data(w_data):
    # Print header for the output table
    header = "Hour\tTemperature (C)\tHumidity (%)\tWeather Description\tRain Probability"
    ret_val = [header]

    # Iterate through each forecast entry and extract relevant data
    bring_umbrella = False
    probability = 0
    weather_description = ""
    pred_time = None
    for entry in w_data['list']:
        weather_id = entry['weather'][0]['id'] # It is int data type
        date_time = str(entry['dt_txt'])  # forecast date and time
        date_time = date_time.split(" ")[1].split(":")[0]
        temperature = entry['main']['temp']  # temperature in °C
        humidity = entry['main']['humidity']  # relative humidity (%)
        description = str(weather_id) + ". " + entry['weather'][0]['description']  # plain description of weather
        rain_probability = float(entry['pop']) * 100
        if weather_id < 700:
            bring_umbrella = True
            if probability < rain_probability:
                probability = rain_probability
                weather_description = description
                pred_time = date_time
        # Print the extracted information in a tab-separated format
        ret_val.append(f"{date_time}\t\t{temperature:.2f}\t\t\t\t{humidity}\t\t\t\t{description}\t\t\t{rain_probability}")
    if bring_umbrella:
        ret_val.append(f"It May Rain. Probability {probability} ({weather_description}) at {pred_time}.")
    else:
        ret_val.append("Weather Is Clear.")
    return ret_val

weather_data = get_weather_data()
ret_val = print_weather_data(weather_data)
email_body = "\n".join(ret_val)
print(email_body)

send_email = EmailFunctions()
send_email.send_email(TO_EMAIL, email_body)