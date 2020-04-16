import functools
from flask import (
    Blueprint,
    request,
    flash,
    redirect,
    render_template,
    url_for,
    session,
    g,
    abort,
)
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
            session["request"] = None
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
