from flask import render_template, current_app, request
from advanced_internet_engineering.app import app, database


@app.route("/index")
def index():
    return render_template("index.html")


@app.route("/<schema>/create", methods=["POST"])
def schema_create(schema):
    content = request.json
    print(content)
    database.create(schema, content)
    return "1"

@app.route("/<schema>/read", methods=["GET"])
def schema_read(schema):
    args = request.args
    if args:
        return database.read(schema, args)
    else:
        return database.read(schema, None)
