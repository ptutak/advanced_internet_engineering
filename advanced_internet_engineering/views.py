from flask import render_template, request, jsonify
from advanced_internet_engineering.app import app


@app.route("/")
def index():
    return render_template("shop/index.html")
