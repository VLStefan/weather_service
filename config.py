import os
from dotenv import load_dotenv

HERE = os.path.dirname(os.path.abspath(__file__))
ENV_PATH = os.path.join(HERE, ".env")
load_dotenv(dotenv_path=ENV_PATH)

HOST = os.getenv("server_host")

DB_URI = os.getenv("db_uri")

API_TOKEN = os.getenv("api_token")


