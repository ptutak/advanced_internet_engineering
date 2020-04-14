import os
from flask import Flask, current_app

app = Flask(__name__)

from advanced_internet_engineering.database import Database

with app.app_context():
    database_path = os.path.join(current_app.root_path, "../database/database.sqlite")
    database = Database(database_path)

from advanced_internet_engineering.auth import auth_blueprint

app.register_blueprint(auth_blueprint)

from advanced_internet_engineering import routes
from advanced_internet_engineering import views
