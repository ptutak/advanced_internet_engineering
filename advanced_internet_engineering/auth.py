from flask import Blueprint, request
from advanced_internet_engineering.app import database

auth_blueprint = Blueprint("auth", __name__, url_prefix="/auth")


@auth_blueprint.route("/register", methods=("GET", "POST"))
def register():
    return ""
