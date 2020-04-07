from flask import render_template, current_app, request, jsonify
from advanced_internet_engineering.app import app, database


@app.route("/index")
def index():
    return render_template("index.html")


@app.route("/<schema>/create", methods=["POST"])
def schema_create(schema):
    content = request.json
    return jsonify(database.create(schema, content))


@app.route("/<schema>/read", methods=["GET"])
def schema_read(schema):
    args = request.args
    if not args:
        args = None
    return jsonify(database.read(schema, args))


@app.route("/<schema>/update/<id_number>", methods=["POST"])
def schema_update(schema, id_number):
    content = request.json
    condition = {"id": id_number}
    return jsonify(database.update(schema, content, condition))
