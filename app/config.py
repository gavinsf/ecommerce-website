from dotenv import load_dotenv
import os

load_dotenv()

class Settings():
    DB_URL = os.getenv("DB")
    DEBUG = True


settings = Settings()