import os
from dotenv import load_dotenv

HERE = os.path.dirname(os.path.abspath(__file__))
ENV_PATH = os.path.join(HERE, ".env")
load_dotenv(dotenv_path=ENV_PATH)

HOST = os.getenv("SERVER_HOST")

DB_URI = os.getenv("DB_URL")

ACCUWEATHER_TOKEN = os.getenv("ACCUWEATHER_TOKEN")

WEATHERSTACK_TOKEN = os.getenv("WEATHERSTACK_TOKEN")


