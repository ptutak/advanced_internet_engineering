import os
import uuid
from flask import Flask, current_app

app = Flask(__name__)

app.secret_key = str(uuid.uuid4())

from advanced_internet_engineering.database import Database

with app.app_context():
    database_path = os.path.join(current_app.root_path, "../database/database.sqlite")
    init = True
    if os.path.isfile(database_path):
        init = False
    database = Database(database_path)
    if init:
        database.create("roles", {"id": 1, "name": "admin"})
        database.create("roles", {"id": 2, "name": "user"})
        database.register("admin", "admin", "admin", "admin")

from advanced_internet_engineering.auth import auth_blueprint

app.register_blueprint(auth_blueprint)

from advanced_internet_engineering import routes
from advanced_internet_engineering import views
