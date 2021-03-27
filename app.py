from flask import Flask, redirect, render_template, url_for, request, jsonify
import stripe
import yaml
import json
from requests import get
from forex_python.converter import CurrencyRates

name = ""
price = 0
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
        print(types)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/Gallery/")
def gallery():
    ip = request.environ.get('HTTP_X_FORWARDED_FOR', "8.8.8.8")
    currency = get(f'https://ipapi.co/{ip}/currency/').text
    curr = c.get_rate('INR', currency)
    return render_template("photos.html", images=images, types=types, currency=curr, symbol=f[currency]["symbol"])


@app.route("/Gallery/<photo>/")
def product(photo):
    ip = request.environ.get('HTTP_X_FORWARDED_FOR', "8.8.8.8")
    currency = get(f'https://ipapi.co/{ip}/currency/').text
    curr = c.get_rate('INR', currency)
    try:
        return render_template("picture.jinja", images=images[photo], name=photo, currency=curr, symbol=f[currency]["symbol"])
    except:
        return render_template("404.jinja")


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.jinja'), 404


if __name__ == "__main__":
    app.run(debug=True)
