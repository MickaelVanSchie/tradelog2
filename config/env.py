import os

from dotenv import load_dotenv


class Environment:
    def __init__(self):
        load_dotenv()  # Load environment variables from .env file

    def __getattr__(self, name):
        return os.getenv(name)

ENV = Environment()