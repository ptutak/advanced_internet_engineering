import requests
from flask import render_template, current_app, request, jsonify, redirect, url_for, g, session, abort, send_from_directory
from advanced_internet_engineering.app import app, database
from advanced_internet_engineering.auth import login_required, admin_required


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(app.root_path, 'favicon.ico', mimetype='image/vnd.microsoft.icon')


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


@app.route("/api/<schema>/create", methods=["POST"])
@admin_required
def schema_create(schema):
    content = request.json
    return jsonify(database.create(schema, content))


@app.route("/api/<schema>/read", methods=["GET"])
@admin_required
def schema_read(schema):
    args = request.args
    if not args:
        args = None
    return jsonify(database.read(schema, args))


@app.route("/api/<schema>/<id_number>", methods=["GET"])
@admin_required
def schema_read_id(schema, id_number):
    args = {"id": id_number}
    return jsonify(database.read(schema, args))


@app.route("/api/<schema>/<id_number>", methods=["PUT"])
@admin_required
def schema_update(schema, id_number):
    content = request.json
    condition = {"id": id_number}
    return jsonify(database.update(schema, content, condition))


@app.route("/api/<schema>/<id_number>", methods=["DELETE"])
@admin_required
def schema_delete(schema, id_number):
    data = {"id": id_number}
    return jsonify(database.delete(schema, data))


@app.route("/myprofile", methods=["GET"])
@login_required
def my_profile():
    data = database.get_profile(g.user["id"])
    return render_template("shop/profile.html", data=data)
