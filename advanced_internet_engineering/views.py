import os.path
import random
import string
from flask import render_template, request, g, redirect, url_for, abort
from advanced_internet_engineering.app import app, database
from advanced_internet_engineering.auth import login_required
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = app.config["UPLOAD_FOLDER"]
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}


@app.route("/")
def index():
    return render_template("shop/index.html")


@app.route("/myprofile", methods=["GET"])
@login_required
def my_profile():
    return render_template("shop/profile.html")


@app.route("/myprofile/edit", methods=["GET", "POST"])
@login_required
def my_profile_edit():
    if request.method == "GET":
        data = database.get_profile(g.user["id"])
        return render_template("shop/profile.html", data=data)
    database.edit_profile(g.user["id_profile"], request.form["profile_content"])
    return redirect(url_for("my_profile"))


@app.before_request
def categories_in_request():
    categories = database.read("product_categories", data=None)
    g.categories = categories


@app.route("/products/<category>", methods=["GET", "POST"])
def products(category):
    if request.method == "POST":
        data = request.form
        data = dict(data)
        if "image" in request.files and request.files["image"]:
            image = request.files["image"]
            filename = secure_filename(image.filename)
            extended_filename = filename
            while os.path.isfile(extended_filename):
                prefix = "".join(random.choices(string.ascii_letters + string.digits, k=8))
                extended_filename = f"{prefix}{filename}"
            data["image"] = extended_filename
            image.save(os.path.join(UPLOAD_FOLDER, extended_filename))
        database.create("products", data)
        return redirect(url_for("products", category=category))
    try:
        id_category = database.read("product_categories", {"name": category})[0]["id"]
        products = database.read("products", {"id_category": id_category})
        categories = database.read("product_categories", data=None)
        return render_template(
            "shop/products.html", products=products, categories=categories, id_category=id_category
        )
    except Exception as e:
        return abort(400, description=str(e))


@app.route("/basket")
def basket():
    return render_template(
        "shop/basket.html"
    )