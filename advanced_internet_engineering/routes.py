from flask import render_template, current_app, request, jsonify
from advanced_internet_engineering.app import app, database


VALID_SCHEMAS = {
    "profile",
    "products",
    "users",
}


class WrongSchema(Exception):
    """
        Raised when the schema selected is not valid
    """


def validate_schema(schema, content):
    if schema not in VALID_SCHEMAS:
        raise WrongSchema(f"Provided schema: {schema}, is not valid")


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


@app.route("/<schema>/<id_number>", methods=["GET"])
def schema_read_id(schema, id_number):
    args = {"id": id_number}
    return jsonify(database.read(schema, args))


@app.route("/<schema>/<id_number>", methods=["PUT"])
def schema_update(schema, id_number):
    content = request.json
    condition = {"id": id_number}
    return jsonify(database.update(schema, content, condition))


@app.route("/<schema>/<id_number>", methods=["DELETE"])
def schema_delete(schema, id_number):
    data = {"id": id_number}
    return jsonify(database.delete(schema, data))
