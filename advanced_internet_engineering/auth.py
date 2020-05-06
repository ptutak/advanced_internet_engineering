import functools

from flask import (Blueprint, abort, flash, g, redirect, render_template,
                   request, session, url_for)

from advanced_internet_engineering.app import database

auth_blueprint = Blueprint("auth", __name__, url_prefix="/auth")


@auth_blueprint.route("/register", methods=("GET", "POST"))
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        try:
            database.register(username, password, "profile content", "user")
            return redirect(url_for("auth.login"))
        except RuntimeError as e:
            flash(str(e))
    return render_template("auth/register.html")


@auth_blueprint.route("/login", methods=("GET", "POST"))
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        try:
            user_id = database.login(username, password)
            session["user_id"] = user_id
            user = database.read("users", {"id": user_id})[0]
            session["profile_id"] = user["id_profile"]
            order_id = session.get("order_id")
            if order_id is not None:
                database.update(
                    "orders", {"id_profile": user["id_profile"]}, {"id": order_id}
                )
            return redirect(url_for("index"))
        except RuntimeError as e:
            flash(str(e))
    return render_template("auth/login.html")


@auth_blueprint.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


@auth_blueprint.before_app_request
def load_logged_in_user():
    user_id = session.get("user_id")

    if user_id is None:
        g.user = None
        g.role = None
    else:
        user = database.read("users", {"id": user_id})[0]
        del user["password"]
        g.user = user
        role = database.read("roles", {"id": user["id_role"]})[0]
        g.role = role["name"]

    profile_id = session.get("profile_id")
    if profile_id is None:
        profile = database.create("profiles", {"profile": "Brak adresu"})
        session["profile_id"] = profile["id"]
        profile_id = profile["id"]
    g.profile_id = profile_id

    order_id = session.get("order_id")
    if order_id is None:
        order = database.create("orders", {"id_profile": profile_id, "id_state": 1})
        session["order_id"] = order["id"]
        order_id = order["id"]
    g.order_id = order_id


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("auth.login"))
        return view(**kwargs)

    return wrapped_view


def admin_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.role != "admin":
            abort(403)
        return view(**kwargs)

    return wrapped_view
