import datetime
import random


class TimeOfDay:
    MORNING = 'morning'
    DAY = 'day'
    EVENING = 'evening'
    NIGHT = 'night'

  
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

time_of_day_emojis = {
    'morning': ['🐳'],
    'day': ['☀️', '🐳'],
    'evening': ['🌆'],
    'night': ['🌙', '🌠', '☄', '🛌', '🌌', '🪐'],
}