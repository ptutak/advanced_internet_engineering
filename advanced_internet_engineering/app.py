import os
import uuid

from flask import Flask, current_app

app = Flask(__name__)

UPLOAD_FOLDER = os.path.abspath(os.path.join(app.root_path, "static"))
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.secret_key = str(uuid.uuid4())


with app.app_context():
    from advanced_internet_engineering.database import Database

    database_path = os.path.join(current_app.root_path, "./database/database.sqlite")
    init = True
    if os.path.isfile(database_path):
        init = False
    database = Database(database_path)
    if init:
        database.create("roles", {"id": 1, "name": "admin"})
        database.create("roles", {"id": 2, "name": "user"})
        database.register("admin", "admin", "admin", "admin")
        database.create(
            "product_categories", {"id": 1, "name": "bathroom", "label": "Bathroom"}
        )
        database.create(
            "product_categories", {"id": 2, "name": "bedroom", "label": "Bedroom"}
        )
        database.create(
            "product_categories", {"id": 3, "name": "kitchen", "label": "Kitchen"}
        )
        database.create("order_states", {"id": 1, "name": "preorder"})
        database.create("order_states", {"id": 2, "name": "ordered"})
        database.create("order_states", {"id": 3, "name": "sent"})


from advanced_internet_engineering.auth import auth_blueprint

app.register_blueprint(auth_blueprint)

from advanced_internet_engineering import routes, views
