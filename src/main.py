from vkbottle.user import User
import datetime
import asyncio
import os

from src.config import STATUS_FORMAT_STR
from src.utils import get_emoji, get_time_of_day
from src.forecast import WeatherManager


class Application:
    def __init__(self) -> None:

        if "{forecast}" in STATUS_FORMAT_STR:
            self.weather_manager = WeatherManager()

        self.user = User(token=os.getenv("TOKEN"))

    async def change_status(self, new_status):
        await self.user.api.status.set(new_status)

    def run(self):
        loop = asyncio.get_event_loop()
        loop.create_task(self.main())
        loop.run_forever()

    async def _get_forecast(self, hour):
        if hasattr(self, "weather_manager"):
            return await self.weather_manager.get_forecast(hour)
        else:
            return None

    async def _generate_status(self):
        current_time = datetime.datetime.now()
        forecast = await self._get_forecast(current_time.hour)
        time_of_day = get_time_of_day(current_time)
        emoji = get_emoji(time_of_day)
        status_time = current_time.strftime("%I:%M %p")
        return STATUS_FORMAT_STR.format(forecast=forecast, emoji=emoji, time=status_time)
    
    async def main(self):
        last_status = None
        while True:
            new_status = await self._generate_status()
            if new_status != last_status:
                await self.change_status(new_status)
                last_status = new_status
            await asyncio.sleep(5)
    

