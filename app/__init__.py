from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import DevelopmentConfig  # Choose the appropriate config for your environment


app = Flask(__name__, template_folder='templates')
app.config.from_object(DevelopmentConfig)

# Continue setting up your app (e.g., database, routes, etc.)

db = SQLAlchemy(app)

from app import routes, models


