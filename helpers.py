import datetime
import random
from enum import Enum
from typing import Literal


class TimeOfDay(Enum):
    MORNING = 'morning'
    DAY = 'day'
    EVENING = 'evening'
    NIGHT = 'night'


time_of_day_emojis = {
    TimeOfDay.MORNING : ['🐳'],
    TimeOfDay.DAY     : ['☀️', '🐳'],
    TimeOfDay.EVENING : ['🌆'],
    TimeOfDay.NIGHT   : ['🌙', '🌠', '🛌', '🌌', '🪐'],
}

def get_time_of_day(
    current_time: datetime.datetime
) -> Literal[TimeOfDay.MORNING, TimeOfDay.DAY, TimeOfDay.EVENING, TimeOfDay.NIGHT]:

    hour = current_time.hour
    if 6 <= hour < 12:
        return TimeOfDay.MORNING
    elif 12 <= hour < 18:
        return TimeOfDay.DAY
    elif 18 <= hour < 24:
        return TimeOfDay.EVENING
    else:
        return TimeOfDay.NIGHT

def get_emoji(time_of_day: TimeOfDay) -> str:
    emoji = time_of_day_emojis.get(time_of_day)
    if isinstance(emoji, list):
        return random.choice(emoji)
    if isinstance(emoji, str):
        return emoji
    else:
        raise ValueError("Invalid value for time_of_day. Expected type TimeOfDay.")
