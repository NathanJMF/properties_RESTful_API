import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
            cls._instance.load_config()
        return cls._instance

    def load_config(self):
        self.__db_host = os.getenv(f"DB_HOST")
        self.__db_port = os.getenv(f"DB_PORT")
        self.__db_name = os.getenv(f"DB_NAME")
        self.__db_user = os.getenv(f"DB_USER")
        self.__db_password = os.getenv(f"DB_PASSWORD")

    @property
    def db_host(self):
        return self.__db_host

    @property
    def db_port(self):
        return self.__db_port

    @property
    def db_name(self):
        return self.__db_name

    @property
    def db_user(self):
        return self.__db_user

    @property
    def db_password(self):
        return self.__db_password
