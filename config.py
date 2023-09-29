import os

class Config:
    DEBUG = False
    TESTING = False
    # Other common configuration options
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:ajit2004@localhost/zomato'
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
