import os
from dotenv import load_dotenv
load_dotenv()


class config:
    DB_USER = os.getenv("DB_USER")
    DB_HOST = os.getenv("DB_HOST")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_NAME = os.getenv("DB_NAME")
    API_URL = os.getenv("API_URL")
    CLIENT_SIDE_URL = os.getenv("CLIENT_SIDE_URL")
