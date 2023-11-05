from vkbottle.user import User
import datetime
import asyncio
from dotenv import load_dotenv
import os
from helpers import get_emoji, get_time_of_day


load_dotenv()

user = User(token=os.getenv('TOKEN'))

async def change_status(new_status):
    await user.api.status.set(new_status)

async def main():
    last_status_time = None
    while True:
        current_time = datetime.datetime.now()
        
        time_of_day = get_time_of_day(current_time)
        
        emoji = get_emoji(time_of_day)
        
        status_time = current_time.strftime("%I:%M %p")
        status_text = f'{status_time} {emoji}'

        if last_status_time != status_time:
            await change_status(status_text)
            last_status_time = status_time

        await asyncio.sleep(5)

if __name__ == '__main__':
    asyncio.run(main())