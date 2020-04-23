import os.path
from flask import render_template, request, g, redirect, url_for, abort
from advanced_internet_engineering.app import app, database
from advanced_internet_engineering.auth import login_required

UPLOAD_FOLDER = os.path.abspath(os.path.join(app.root_path, "static"))
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}


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


@app.route("/products/<category>", methods=["GET", "POST"])
def products(category):
    if request.method == "POST":
        data = request.form
        data = dict(data)
        print(request.files)
        if "image" in request.files and request.files["image"]:
            image = request.files["image"]
            data["image"] = image.filename
            image.save(os.path.join(UPLOAD_FOLDER, image.filename))
        print(data)
        database.create("products", data)
        return redirect(url_for("products", category=category))
    try:
        id_category = database.read("product_categories", {"name": category})[0]["id"]
        products = database.read("products", {"id_category": id_category})
        categories = database.read("product_categories", data=None)
        return render_template(
            "shop/products.html", products=products, categories=categories
        )
    except Exception as e:
        return abort(400, description=str(e))
