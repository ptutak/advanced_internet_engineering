from flask import Blueprint, request, flash, redirect, render_template, url_for
from advanced_internet_engineering.app import database

auth_blueprint = Blueprint("auth", __name__, url_prefix="/auth")


@auth_blueprint.route("/register", methods=("GET", "POST"))
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        try:
            database.register(username, password)
            return redirect(url_for("advanced_internet_engineering.auth.login"))
        except RuntimeError as e:
            flash(str(e))
    return render_template("auth/register.html")


@auth_blueprint.route("/login", methods=("GET", "POST"))
def login():
    pass
