import requests
import os
from twilio.rest import Client

API_KEY = "c7c188e45319e9b89a3b38d619e4015c"
LATITUDE = -7.531940
LONGITUDE = 111.073051
OWN_ENDPOINT = "https://api.openweathermap.org/data/2.5/onecall"

weather_params = {
    "lat": LATITUDE,
    "lon": LONGITUDE,
    "appid": API_KEY,
    "exclude": "current,minutely,daily"
}

account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']

response = requests.get(OWN_ENDPOINT, params=weather_params)
response.raise_for_status()

weather_data = response.json()
weather_slice = weather_data["hourly"][:12]

will_rain = False

for hour_data in weather_slice:
    condition_code = hour_data["weather"][0]["id"]

    if int(condition_code) < 700:
        will_rain = True

if will_rain:
    client = Client(account_sid, auth_token)
    message = client.messages \
        .create(
            body="It's going to rain today, remember to brain an umbrella.",
            from_='+15017122661',
            to='+15558675310'
        )


