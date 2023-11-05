import requests
import json
import os
import logging


ACCUWEATHER_API_KEY = os.getenv('ACCUWEATHER_API_KEY')

def get_location_key():
    try:
        location_key_url = f'http://dataservice.accuweather.com/locations/v1/cities/search?apikey={ACCUWEATHER_API_KEY}&q={os.getenv("CITY")}'
        location_key_query = requests.get(location_key_url)
        location_key = json.loads(location_key_query.text)
        logging.info('LOCATION_KEY has been successufly parsed.')
        return location_key[0]["Key"]
    except KeyError:
        logging.error('Error while parsing LOCATION_KEY.')

LOCATION_KEY = get_location_key()

cache = {}

def get_forecast(hours):
    if cache.get(hours):
        return cache.get(hours)
    try:
        response = requests.get(f'http://dataservice.accuweather.com/currentconditions/v1/{LOCATION_KEY}?apikey={ACCUWEATHER_API_KEY}&language=en&details=true&metric=true')
        forecast = json.loads(response.text)
        current_temperature = forecast[0]['Temperature']['Metric']['Value']
        cache.clear()
        cache[hours] = f'{current_temperature} ℃'
        return f'{current_temperature} ℃'
    except KeyError:
        return None
