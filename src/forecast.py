import requests
import aiohttp

from src.logger import logger
from src.config import CITY, ACCUWEATHER_API_KEY


class WeatherManager:
    def __init__(self):
        self.location_key = self.__get_location_key(CITY)
        self.forecast_cache = {}

    def __get_location_key(self, city):
        try:
            location_key_url = f"http://dataservice.accuweather.com/locations/v1/cities/search?apikey={ACCUWEATHER_API_KEY}&q={city}"
            location_key_query = requests.get(location_key_url)
            location_key_data = location_key_query.json()
            location_key = location_key_data[0]["Key"]
            logger.info("LOCATION_KEY has been successfully parsed.")
            return location_key
        except (IndexError, KeyError):
            logger.error("Error while parsing LOCATION_KEY.")
            return None

    async def __get_current_temperature(self):
        try:
            url = f"http://dataservice.accuweather.com/currentconditions/v1/{self.location_key}?apikey={ACCUWEATHER_API_KEY}&language=en&details=true&metric=true"
            response = await self.__get_request_json(url)
            current_temperature = response[0]["Temperature"]["Metric"]["Value"]
            return f"{current_temperature} ℃"
        except (IndexError, KeyError):
            logger.error("Error while retrieving current temperature.")
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
