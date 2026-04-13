import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("WEATHER_API_KEY")

api_url = "https://api.weatherapi.com/v1/current.json" #API endpoint for current weather

#must place this before params since the next block specifies 90045
zip_codes = ["90045", "10001", "60601", "98101", "33101"]

for zip_code in zip_codes:
    params = {
        "key": API_KEY,
        "q": zip_code
    }

    response = requests.get(api_url, params=params)
    data = response.json()

    city = data["location"]["name"]
    temp = data["current"]["temp_f"]
    condition = data["current"]["condition"]["text"]

    print(f"{city}: {temp}°F, {condition}")

    '''

    response = requests.get(api_url, params=params)

    # print(response) 

    data = response.json() #converting the data this API gets to json object and printing it out
    # print(json.dumps(data, indent=4))

    # now im getting the current object only, wanting to see the farenheight temp 
    print(data["current"]["temp_f"])
    '''