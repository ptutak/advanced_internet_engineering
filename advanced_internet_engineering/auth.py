import functools
from flask import Blueprint, request, flash, redirect, render_template, url_for, session, g
from advanced_internet_engineering.app import database

auth_blueprint = Blueprint("auth", __name__, url_prefix="/auth")


@auth_blueprint.route("/register", methods=("GET", "POST"))
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        try:
            database.register(username, password)
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
            return redirect(url_for("views.index"))
        except RuntimeError as e:
            flash(str(e))
    return render_template("auth/login.html")


@auth_blueprint.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("views.index"))


@auth_blueprint.before_app_request
def load_logged_in_user():
    user_id = session.get("user_id")

    if user_id is None:
        g.user = None
    else:
        user = database.read("users", {"id": user_id})
        del user["password"]
        g.user = user


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("auth.login"))
        return view(**kwargs)
    return wrapped_view
