import os
from dotenv import load_dotenv

from src.logger import logger


load_dotenv()


STATUS_FORMAT_STR: str = os.getenv("STATUS_FORMAT", "{time} {emoji} | {forecast}")

if not os.getenv("STATUS_FORMAT"):
    logger.warning("Environment variable STATUS_FORMAT not found, using default format")

TOKEN = os.getenv("TOKEN")

if not TOKEN:
    logger.error("Environment variable TOKEN is not specified")
    exit(1)

ACCUWEATHER_API_KEY = os.getenv("ACCUWEATHER_API_KEY")
if not ACCUWEATHER_API_KEY:
    logger.warning("Environment variable ACCUWEATHER_API_KEY is not specified")

CITY = os.getenv("CITY")

if ACCUWEATHER_API_KEY and not CITY:
    logger.warning("Environment variable CITY is not specified")
    exit(1)
