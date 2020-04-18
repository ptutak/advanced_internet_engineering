import requests
from flask import (
    render_template,
    current_app,
    request,
    jsonify,
    redirect,
    url_for,
    g,
    session,
    abort,
    send_from_directory,
)
from advanced_internet_engineering.app import app, database
from advanced_internet_engineering.auth import login_required, admin_required


@app.route("/favicon.ico")
def favicon():
    return send_from_directory(
        app.root_path, "favicon.ico", mimetype="image/vnd.microsoft.icon"
    )


@app.route("/api/<schema>/create", methods=["POST"])
@admin_required
def schema_create(schema):
    content = request.json
    try:
        return jsonify(database.create(schema, content))
    except Exception as e:
        return str(e)


@app.route("/api/<schema>/read", methods=["GET"])
@admin_required
def schema_read(schema):
    args = request.args
    if not args:
        args = None
    try:
        return jsonify(database.read(schema, args))
    except Exception as e:
        return {"error": str(e)}


@app.route("/api/<schema>/<id_number>", methods=["GET"])
@admin_required
def schema_read_id(schema, id_number):
    args = {"id": id_number}
    try:
        return jsonify(database.read(schema, args))
    except Exception as e:
        return {"error": str(e)}


@app.route("/api/<schema>/<id_number>", methods=["PUT"])
@admin_required
def schema_update(schema, id_number):
    content = request.json
    condition = {"id": id_number}
    try:
        return jsonify(database.update(schema, content, condition))
    except Exception as e:
        return {"error": str(e)}


@app.route("/api/<schema>/<id_number>", methods=["DELETE"])
@admin_required
def schema_delete(schema, id_number):
    data = {"id": id_number}
    try:
        return jsonify(database.delete(schema, data))
    except Exception as e:
        return {"error": str(e)}


@app.route("/myprofile", methods=["GET"])
@login_required
def my_profile():
    data = database.get_profile(g.user["id"])
    return render_template("shop/profile.html", data=data)


@app.route("/myprofile/edit", methods=["GET", "POST"])
@login_required
def my_profile_edit():
    if request.method == "GET":
        data = database.get_profile(g.user["id"])
        return render_template("shop/profile.html", data=data)
    database.edit_profile(g.user["id_profile"], request.form["profile_content"])
    return redirect(url_for("my_profile"))
