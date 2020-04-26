import os
import os.path

from flask import abort, jsonify, request, send_from_directory

from advanced_internet_engineering.app import app, database
from advanced_internet_engineering.auth import admin_required

UPLOAD_FOLDER = app.config["UPLOAD_FOLDER"]


@app.route("/favicon.ico")
def favicon():
    return send_from_directory(
        app.root_path, "favicon.ico", mimetype="image/vnd.microsoft.icon"
    )


@app.route("/api/v1/<schema>", methods=["POST"])
@admin_required
def schema_create(schema):
    content = request.json
    try:
        return jsonify(database.create(schema, content))
    except Exception as e:
        return abort(400, description=str(e))


@app.route("/api/v1/<schema>", methods=["GET"])
@admin_required
def schema_read(schema):
    args = request.args
    if not args:
        args = None
    try:
        return jsonify(database.read(schema, args))
    except Exception as e:
        return abort(400, description=str(e))


@app.route("/api/v1/<schema>/<id_number>", methods=["GET"])
@admin_required
def schema_read_id(schema, id_number):
    args = {"id": id_number}
    try:
        return jsonify(database.read(schema, args))
    except Exception as e:
        return abort(400, description=str(e))


@app.route("/api/v1/<schema>/<id_number>", methods=["PUT"])
@admin_required
def schema_update(schema, id_number):
    content = request.json
    condition = {"id": id_number}
    try:
        return jsonify(database.update(schema, content, condition))
    except Exception as e:
        return abort(400, description=str(e))


@app.route("/api/v1/<schema>/<id_number>", methods=["DELETE"])
@admin_required
def schema_delete(schema, id_number):
    data = {"id": id_number}
    if schema == "products":
        product = database.read(schema, data)
    try:
        result = jsonify(database.delete(schema, data))
    except Exception as e:
        return abort(400, description=str(e))
    if schema == "products" and product["image"]:
        image_path = os.path.join(UPLOAD_FOLDER, product["image"])
        if os.path.isfile(image_path):
            os.remove(os.path.join(UPLOAD_FOLDER, product["image"]))
    return result
