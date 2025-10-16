import os
from dotenv import load_dotenv
load_dotenv()

class Config:
    DEBUG = os.getenv("FLASK_ENV", "production") == "development"
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:postgres@localhost:5433/nyc_taxi_db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", 50000))
    BATCH_SIZE = int(os.getenv("BATCH_SIZE", 5000))
    HOST = os.getenv("FLASK_RUN_HOST", "0.0.0.0")
    PORT = int(os.getenv("FLASK_RUN_PORT", 7070))
