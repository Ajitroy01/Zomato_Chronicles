import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Access the environment variables
DATABASE_URL = os.getenv("DATABASE_URL")
class Config:
    DEBUG = False
    TESTING = False
    # config.py
    SQLALCHEMY_DATABASE_URI = DATABASE_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Disable tracking modifications for better performance

class DevelopmentConfig(Config):
    DEBUG = True
    # Development-specific configurations

class ProductionConfig(Config):
    DEBUG = False
    # Production-specific configurations

class TestConfig:
    SQLALCHEMY_DATABASE_URI = "sqlite:///test.db"  # Use an SQLite database for testing
    TESTING = True
