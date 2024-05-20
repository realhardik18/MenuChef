from creds import WEATHER_API_KEY,WEATHER_API_URL
import requests

def get_weather(city):
    response = requests.get(
        WEATHER_API_URL+city.format(city),
        headers={'X-Api-Key': WEATHER_API_KEY})
    print(response.text)

