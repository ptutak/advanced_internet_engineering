import os.path
from flask import render_template, current_app
from advanced_internet_engineering.app import app


@app.route("/index")
def index():
    return render_template("index.html")
