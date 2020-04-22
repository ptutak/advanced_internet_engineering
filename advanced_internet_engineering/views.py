from flask import render_template, request, g, redirect, url_for, abort
from advanced_internet_engineering.app import app, database
from advanced_internet_engineering.auth import login_required


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


@app.route("/products/<category>", methods=["GET"])
def products(category):
    try:
        id_category = database.read("product_categories", {"name": category})[0]["id"]
        products = database.read("products", {"id_category": id_category})
        return render_template("shop/products.html", products=products)
    except Exception as e:
        return abort(400, description=str(e))
