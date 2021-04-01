from flask import Flask, redirect, render_template, url_for, request, jsonify, abort
import stripe
import yaml
import json
from requests import get
from forex_python.converter import CurrencyRates

name = ""
price = 0
currency = "USD"
stripe.api_key = "sk_test_51IXQeCSJIrO4r1c2upI16Js4ULKmplnErq7W77lEEFxPRDEZqPEgMoz8kFk26Et74gu4LRb7DjE5NOFc8xj5nEkM00hD099iy4"

with open("db.yaml", "r") as y:
    db = yaml.load(y, yaml.FullLoader)

with open("Currency.json", "r", encoding="utf-8") as f:
    f = json.loads(f.read())

images = db["images"]
app = Flask(__name__)
c = CurrencyRates()

types = []
types.append("All")
for i in images:
    if not images[i]["type"] in types:
        types.append(images[i]["type"])


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/Gallery/")
def gallery():
    global currency
    ip = request.environ.get('HTTP_X_FORWARDED_FOR', "8.8.8.8")
    currency = get(f'https://ipapi.co/{ip}/currency/').text
    curr = c.get_rate('INR', currency)
    return render_template("photos.html", images=images, types=types, currency=curr, symbol=f[currency]["symbol"])


@app.route("/info", methods=["POST"])
def info():
    global name, price
    name = request.get_json().get('name')
    price = request.get_json().get('price')
    return ""


cus_name, phone, address1, address2, city, state, country, postal = "", "", "", "", "", "", "", ""


@app.route("/customer", methods=["GET", "POST"])
def customer():
    if request.method == "GET":
        print(request.headers)
        print("Referer" in request.headers)
        if "Referer" in request.headers:
            return render_template("info.html")
        else:
            abort(404)
    else:
        global cus_name, phone, address1, address2, postal, city, state, country
        cus_name, phone, address1, address2, city, state, country, postal = request.get_json().get('cus_name'), request.get_json().get("phone"), request.get_json().get(
            "address1"), request.get_json().get("address2"), request.get_json().get("city"), request.get_json().get("state"), request.get_json().get("country"), request.get_json().get("postal")
        return ""


@app.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
    global name, price, currency, cus_name, address1, phone, address2, city, state, postal, country
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        payment_intent_data={
            "shipping": {
                "name": cus_name,
                "address": {
                    "line1": address1,
                    "line2": address2,
                    "city": city,
                    "postal_code": postal,
                    "country": country,
                    "state": state
                },
                "phone": phone
            }
        },
        line_items=[{
            'price_data': {
                'currency': currency,
                'product_data': {
                    'name': name,
                    'images': [url_for("static", filename="images/bg1.jpg", _external=True)],
                },
                'unit_amount': int(float(price) * 100),
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url=url_for("gallery", _external=True),
        cancel_url=url_for("gallery", _external=True),
    )
    return jsonify(id=session.id)


@app.route("/Gallery/<photo>/")
def product(photo):
    ip = request.environ.get('HTTP_X_FORWARDED_FOR', "8.8.8.8")
    currency = get(f'https://ipapi.co/{ip}/currency/').text
    curr = c.get_rate('INR', currency)
    try:
        return render_template("picture.html", images=images[photo], name=photo, currency=curr, symbol=f[currency]["symbol"])
    except:
        return render_template("404.jinja")


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.jinja'), 404


@app.errorhandler(405)
def page_not_found(e):
    return render_template('404.jinja'), 405


if __name__ == "__main__":
    app.run(debug=True)
