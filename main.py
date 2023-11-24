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
    """
    The Application class manages the status of a user in a messaging application.
    
    Attributes:
    - status_format_str (str): Format string for the user's status message.
    - weather_manager (WeatherManager): Manages weather information if forecast is included in the status format.
    - user (User): Represents the user with a specified token.

    Methods:
    - __init__(self): Initializes the Application object.
    - change_status(self, new_status): Asynchronously changes the user's status.
    - run(self): Runs the main event loop to update the user's status periodically.
    - __get_forecast(self, hour): Asynchronously retrieves weather information for a specified hour using the WeatherManager class.
    - main(self): The main asynchronous function that updates the user's status based on the configured format.
    """
    def __init__(self) -> None:
        self.status_format_str: str = os.getenv(
            "STATUS_FORMAT", "{time} {emoji} | {forecast}"
        )
        if not os.getenv("STATUS_FORMAT"):
            logging.warning(
                "Environment variable STATUS_FORMAT not found, using default format"
            )

        if "{forecast}" in self.status_format_str:
            self.weather_manager = WeatherManager()

        self.user = User(token=os.getenv("TOKEN"))

    async def change_status(self, new_status):
        await self.user.api.status.set(new_status)

    def run(self):
        loop = asyncio.get_event_loop()
        loop.create_task(self.main())
        loop.run_forever()

    async def __get_forecast(self, hour):
        if hasattr(self, "weather_manager"):
            return await self.weather_manager.get_forecast(hour)
        else:
            return None

    async def main(self):
        last_time = None
        while True:
            current_time = datetime.datetime.now()
            forecast = await self.__get_forecast(current_time.hour)
            time_of_day = get_time_of_day(current_time)
            emoji = get_emoji(time_of_day)
            status_time = current_time.strftime("%I:%M %p")

            status_formated_string = self.status_format_str.format(
                forecast=forecast, emoji=emoji, time=status_time
            )

            if last_time != status_time:
                await self.change_status(status_formated_string)
                last_time = status_time

            await asyncio.sleep(5)


if __name__ == "__main__":
    app = Application()
    app.run()
