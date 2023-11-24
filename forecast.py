import requests
import os
import logging
import aiohttp


class WeatherManager:
    """
    The WeatherManager class provides functionality for getting weather information using the AccuWeather API.

    Attributes:
    - ACCUWEATHER_API_KEY (str): AccuWeather API key obtained from environment variables.
    - location_key (str): Location key for the specified city.
    - forecast_cache (dict): Cache for storing forecasts for specific hours.

    Methods:
    - __init__(self): Initializes the WeatherManager object.
    - __get_location_key(self, city): Retrieves the location key for the specified city.
    - __get_current_temperature(self): Asynchronously obtains the current temperature for the specified location.
    - __get_request_json(url): Performs an asynchronous HTTP request and returns data in JSON format.
    - get_forecast(self, hour): Retrieves the forecast for a specific hour using the cache.
    - __get_last_cached_value(self): Retrieves the last value from the forecast cache.
    """
    def __init__(self):
        self.ACCUWEATHER_API_KEY = os.getenv("ACCUWEATHER_API_KEY")
        if not self.ACCUWEATHER_API_KEY:
            logging.warning("Environment variable ACCUWEATHER_API_KEY is not specified")
            exit(1)

        if not os.getenv("CITY"):
            logging.warning("Environment variable CITY is not specified")
            exit(1)

        self.location_key = self.__get_location_key(os.getenv("CITY"))
        self.forecast_cache = {}

    def __get_location_key(self, city):
        try:
            location_key_url = f"http://dataservice.accuweather.com/locations/v1/cities/search?apikey={self.ACCUWEATHER_API_KEY}&q={city}"
            location_key_query = requests.get(location_key_url)
            location_key_data = location_key_query.json()
            location_key = location_key_data[0]["Key"]
            logging.info("LOCATION_KEY has been successfully parsed.")
            return location_key
        except (IndexError, KeyError):
            logging.error("Error while parsing LOCATION_KEY.")
            return None

    async def __get_current_temperature(self):
        try:
            url = f"http://dataservice.accuweather.com/currentconditions/v1/{self.location_key}?apikey={self.ACCUWEATHER_API_KEY}&language=en&details=true&metric=true"
            response = await self.__get_request_json(url)
            current_temperature = response[0]["Temperature"]["Metric"]["Value"]
            return f"{current_temperature} ℃"
        except (IndexError, KeyError):
            logging.error("Error while retrieving current temperature.")
            return None

    @staticmethod
    async def __get_request_json(url):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                return await response.json()

    async def get_forecast(self, hour):
        if self.forecast_cache.get(hour):
            return self.forecast_cache[hour]

        current_temperature = await self.__get_current_temperature()

        if current_temperature:
            self.forecast_cache.clear()
            self.forecast_cache[hour] = current_temperature
            return current_temperature
        else:
            return self.__get_last_cached_value()

    def __get_last_cached_value(self):
        try:
            _, value = self.forecast_cache.popitem()
            return value
        except KeyError:
            return None
