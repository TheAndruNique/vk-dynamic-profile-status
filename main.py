from vkbottle.user import User
import datetime
import asyncio
from dotenv import load_dotenv
import os
import random


load_dotenv()

user = User(token=os.getenv('TOKEN'))

class TimeOfDay:
    MORNING = 'morning'
    DAY = 'day'
    EVENING = 'evening'
    NIGHT = 'night'

time_of_day_emojis = {
    'morning': ['🐳'],
    'day': ['☀️', '🐳'],
    'evening': ['🌆'],
    'night': ['🌙', '🌠', '☄', '🛌', '🌌', '🪐'],
}

async def change_status(new_status):
    await user.api.status.set(new_status)

def get_time_of_day(current_time: datetime.datetime):
    hour = current_time.hour
    if 6 <= hour < 12:
        return TimeOfDay.MORNING
    elif 12 <= hour < 18:
        return TimeOfDay.DAY
    elif 18 <= hour < 24:
        return TimeOfDay.EVENING
    else:
        return TimeOfDay.NIGHT

def get_emoji(time_of_day):
    emoji = time_of_day_emojis.get(time_of_day)
    if isinstance(emoji, list):
        return random.choice(emoji)
    if isinstance(emoji, str):
        return emoji

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