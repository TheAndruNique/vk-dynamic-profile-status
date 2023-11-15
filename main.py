from vkbottle.user import User
import datetime
import asyncio
from dotenv import load_dotenv
import os
from helpers import get_emoji, get_time_of_day
from forecast import WeatherManager
import logging


load_dotenv()


class Application:
    def __init__(self) -> None:
        self.status_format_str: str = os.getenv('STATUS_FORMAT', '{time} {emoji} | {forecast}')
        if not os.getenv('STATUS_FORMAT'):
            logging.warning('Environment variable STATUS_FORMAT not found, using default format')

        self.weather_manager = WeatherManager()
        self.user = User(token=os.getenv('TOKEN'))

    async def change_status(self, new_status):
        await self.user.api.status.set(new_status)
    
    def run(self):
        asyncio.run(self.main())
    
    async def main(self):
        last_time = None
        while True:
            current_time = datetime.datetime.now()
            forecast = self.weather_manager.get_forecast(current_time.hour)
            time_of_day = get_time_of_day(current_time)
            emoji = get_emoji(time_of_day)
            status_time = current_time.strftime("%I:%M %p")
            
            status_formated_string = self.status_format_str.format(
                forecast = forecast,
                emoji = emoji,
                time = status_time
            )
            
            if last_time != status_time:
                await self.change_status(status_formated_string)
                last_time = status_time

            await asyncio.sleep(5)
            


if __name__ == '__main__':
    app = Application()
    app.run()
    