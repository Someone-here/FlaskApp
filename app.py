from flask import Flask, redirect, render_template, url_for, request, jsonify, abort, session
import stripe
import yaml
import json
from requests import get
from forex_python.converter import CurrencyRates

with open("db.yaml", "r") as y:
    db = yaml.load(y, yaml.FullLoader)

with open("Currency.json", "r", encoding="utf-8") as f:
    f = json.loads(f.read())

images = db["images"]
app = Flask(__name__)
app.secret_key = "ngU*)({:&^&&9853{>:()*I:>4uv]\}:{>[34k/3tvh3(*&^%$h859!@#$lko[px790f8t98"
stripe.api_key = "sk_test_51IdTodSIXcXkEUKCWr4dnzUSkjQGhvxGfzlESoMUg6ju3QMtWOnQiWEaLU9A3aessVHsZC5HOWc1hXS8OFemBAi200OoE7GZ2u"
c = CurrencyRates()

types = []
types.append("All")
for i in images:
    if not images[i]["type"] in types:
        types.append(images[i]["type"])


def get_currency():
    try:
        ip = request.environ['HTTP_X_FORWARDED_FOR']
        currency = get(f'https://ipapi.co/{ip}/currency/').text
    except:
        currency = "USD"
    return currency


# @app.before_request
# def before_request():
#     if request.url.startswith('http://'):
#         url = request.url.replace('http://', 'https://', 1)
#         code = 301
#         return redirect(url, code=code)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/Gallery/")
def gallery():
    try:
        session.pop("cus_info", None)
        session.clear()
    except:
        pass
    finally:
        currency = get_currency()
        curr = c.get_rate('INR', currency)
        return render_template("photos.html", images=images, types=types, currency=curr, symbol=f[currency]["symbol"])


@app.route("/info", methods=["POST"])
def info():
    currency = get_currency()
    curr = c.get_rate('INR', currency)
    if request.get_json().get("request") == "setup":
        if request.get_json().get('name') in images:
            session["name"] = request.get_json().get('name')
            session["image"] = request.get_json().get("image")
        else:
            return None
    if request.get_json().get("request") == "Variants":
        session["quantity"] = request.get_json().get("quantity")
        if request.get_json().get("frame") in images[session["name"]]:
            session["frame"] = request.get_json().get("frame")
        if request.get_json().get("size") in images[session["name"]][session["frame"]]:
            session["size"] = request.get_json().get("size")

        output = round(images[session["name"]]
                       [session["frame"]][session["size"]] * curr, 2)
        session["price"] = output
        return {"price": output}

    return ""


@app.route("/customer", methods=["GET", "POST"])
def customer():
    if request.method == "GET":
        if "Referer" in request.headers:
            return render_template("customer.html")
        else:
            abort(404)
    else:
        try:
            session.pop("cus_info", None)
        except:
            pass
        finally:
            data = request.get_json()
            session["cus_info"] = data
            session.modified = True
            return ""


@app.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
    session.modified = True
    data = session["cus_info"]
    currency = get_currency()
    Session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        payment_intent_data={
            "metadata": {
                "Frame": session["frame"],
                "Size": session["size"]
            },
            "shipping": {
                "name": data["cus_name"],
                "address": {
                    "line1": data["address1"],
                    "line2": data["address2"],
                    "city": data["city"],
                    "postal_code": data["postal"],
                    "country": data["country"],
                    "state": data["state"]
                },
                "phone": data["phone"]
            }
        },
        customer_email=data["email"],
        metadata={
            "Frame": session["frame"],
            "Size": session["size"]
        },
        line_items=[{
            'price_data': {
                'currency': currency,
                'product_data': {
                    'name': session["name"],
                    'images': [url_for("static", filename=session["image"], _external=True)],
                },
                'unit_amount': int(float(session["price"]) * 100),
            },
            'quantity': session["quantity"],
        }],
        mode='payment',
        success_url=url_for("gallery", _external=True),
        cancel_url=url_for("gallery", _external=True),
    )
    return jsonify(id=Session.id)


@app.route("/Gallery/<photo>/")
def product(photo):
    try:
        session.pop("cus_info", None)
        session.clear()
    except:
        pass
    finally:
        currency = get_currency()
        curr = c.get_rate('INR', currency)
        try:
            return render_template("picture.html", images=images[photo], name=photo, currency=curr, symbol=f[currency]["symbol"])
        except:
            abort(404)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.jinja'), 404


@app.errorhandler(405)
def page_not_found(e):
    return render_template('404.jinja'), 405


if __name__ == "__main__":
    app.run(debug=True)
