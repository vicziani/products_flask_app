from flask import Flask, current_app, redirect, render_template, request
import pyodbc

app = Flask(__name__)
app.template_folder = "templates"

app.config.from_mapping(
    CONN_STR = (
        r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'
        r'DBQ=C:\trainings\products-flask-app\products.accdb;'
    )
)

@app.route("/", methods=["GET"])
def list_products():
    print("List products")

    conn = pyodbc.connect(current_app.config["CONN_STR"])
    curs = conn.cursor()
    products = []
    for id, name in curs.execute("select id, product_name from products"):
        print("Product: ", id, name)
        products.append({"id": id, "name": name})

    return render_template("products.html", message="Kenyér", products_in_html=products)

@app.route("/", methods=["POST"])
def save_product():
    print("Save product")

    product_name = request.form.get("form-product-name")
    print("Product name", product_name)

    conn = pyodbc.connect(current_app.config["CONN_STR"])
    curs = conn.cursor()
    curs.execute("insert into products(product_name) values (?)", product_name)
    conn.commit()

    return redirect("/")