import os
import dotenv

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "my_secrete_key")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///data.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    API_URL = os.getenv("API_URL", "http://localhost:8000/api")
