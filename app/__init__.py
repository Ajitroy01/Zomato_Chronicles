from flask import Flask
from app.menu import menu_bp
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from app.models import db
from app.staff import staff_bp
from app.auth import auth_bp
from flask_cors import CORS
from flask_login import LoginManager

def create_app(config_name="development"):
    app = Flask(__name__)
    login_manager = LoginManager(app)
    
    # Set the secret key
    app.secret_key = 'aprqrst12359'

    
    CORS(app, origins="*")
    # Load configuration based on the 'config_name' argument (e.g., 'development', 'production', etc.)
    if config_name == "development":
        app.config.from_object("config.DevelopmentConfig")
    elif config_name == "production":
        app.config.from_object("config.ProductionConfig")
    elif config_name == "test":
        app.config.from_object("config.TestConfig")
    
    # Initialize the database with the MySQL database URI
    app.config['SQLALCHEMY_DATABASE_URI'] = app.config['SQLALCHEMY_DATABASE_URI']
    db.init_app(app)

    # Import and register blueprints here (we'll do this in later steps).
    app.register_blueprint(menu_bp)
    app.register_blueprint(staff_bp)
    app.register_blueprint(auth_bp)

    # Initialize Flask-Migrate
    migrate = Migrate(app, db)

    return app
