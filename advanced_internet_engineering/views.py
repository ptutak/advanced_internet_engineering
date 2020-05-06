import os.path
import random
import string

from flask import (abort, g, redirect, render_template, request, session,
                   url_for)
from werkzeug.utils import secure_filename

from advanced_internet_engineering.app import app, database
from advanced_internet_engineering.auth import login_required, admin_required

UPLOAD_FOLDER = app.config["UPLOAD_FOLDER"]
ALLOWED_EXTENSIONS = {"txt", "pdf", "png", "jpg", "jpeg", "gif"}


@app.route("/")
def index():
    return render_template("shop/index.html")


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


@app.before_request
def categories_in_request():
    categories = database.read("product_categories", data=None)
    g.categories = categories


@app.before_request
def default_order_profile():
    if "profile" not in session:
        session["profile"] = database.create("profiles", {"profile": "None"})

    if "order" not in session:
        session["order"] = database.create(
            "orders", {"id_profile": session["profile"]["id"], "id_state": 1}
        )

    g.profile = session["profile"]
    g.order = session["order"]


@app.route("/products/<category>", methods=["GET", "POST"])
def products(category):
    if request.method == "POST":
        return redirect(url_for("products_add", category=category))
    try:
        id_category = database.read("product_categories", {"name": category})[0]["id"]
        products = database.read("products", {"id_category": id_category})
        categories = database.read("product_categories", data=None)
        return render_template(
            "shop/products.html",
            products=products,
            categories=categories,
            id_category=id_category,
        )
    except Exception as e:
        return abort(400, description=str(e))


@app.route("/products_add/<category>", methods=["POST"])
@admin_required
def products_add(category):
    data = request.form
    data = dict(data)
    if "image" in request.files and request.files["image"]:
        image = request.files["image"]
        filename = secure_filename(image.filename)
        extended_filename = filename
        while os.path.isfile(extended_filename):
            prefix = "".join(
                random.choices(string.ascii_letters + string.digits, k=8)
            )
            extended_filename = f"{prefix}{filename}"
        data["image"] = extended_filename
        image.save(os.path.join(UPLOAD_FOLDER, extended_filename))
    database.create("products", data)
    return redirect(url_for("products", category=category), code=303)


@app.route("/product/get/<id_product>", methods=["GET"])
def product(id_product):
    try:
        product = database.read("products", {"id": id_product})[0]
        return render_template("shop/product.html", product=product)
    except Exception as e:
        return abort(400, description=str(e))


@app.route("/product/add_to_basket/<id_product>", methods=["PUT"])
def add_to_basket(id_product):
    database.create("baskets", {"id_order": g.order_id, "id_product": id_product})
    return redirect(url_for("product", id_product=id_product), code=303)


@app.route("/basket")
def basket():
    products_in_basket = database.get_order(g.order_id)
    return render_template("shop/basket.html", products=products_in_basket)
