from flask import Flask, redirect, render_template, url_for, request, jsonify, abort, session
import stripe
import yaml
import math
import json
import urllib3
from bs4 import BeautifulSoup

http = urllib3.PoolManager()

with open("db.yaml", "r") as y:
    db = yaml.load(y, yaml.FullLoader)

with open("Currency.json", "r", encoding="utf-8") as f:
    f = json.loads(f.read())

images = db["images"]
app = Flask(__name__)
app.secret_key = "ngU*)({:&^&&9]853{>:()*I:>43u%v]\}:{__vr_>[34k%/673t{}[[[vh3(*&^%$h3$_54_43__859!@#$l=#+333ko[px790f8t98"
stripe.api_key = "sk_test_51IdTodSIXcXkEUKCWr4dnzUSkjQGhvxGfzlESoMUg6ju3QMtWOnQiWEaLU9A3aessVHsZC5HOWc1hXS8OFemBAi200OoE7GZ2u"

def get_rate(cur1, cur2):
    r = http.request('GET', f'https://www.google.com/finance/quote/{cur1}-{cur2}').data
    soup = BeautifulSoup(r, features="html.parser")
    
    print(soup[0: 25], str(r)[0: 25])
    print(soup.select("div.YMlKec.fxKbKc").text)
    return float(soup.select("div.YMlKec.fxKbKc")[0].text)

types = []
types.append("All")
for i in images:
    if not images[i]["type"] in types:
        types.append(images[i]["type"])


def get_currency():
    try:
        ip = request.environ['HTTP_X_FORWARDED_FOR']
        currency = http.request('GET', f'https://ipapi.co/{ip}/currency/').data
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
        curr = get_rate('INR', currency)
        return render_template("photos.html", images=images, types=types, currency=curr, symbol=f[currency]["symbol"])


@app.route("/info", methods=["POST"])
def info():
    currency = get_currency()
    curr = get_rate('INR', currency)
    if request.get_json().get("request") == "setup":
        if request.get_json().get('name') in images:
            session["name"] = request.get_json().get('name')
            session["image"] = request.get_json().get("image")
            print(session["name"], session["image"])
            session.modified = True
        else:
            return "Stop it"
    if request.get_json().get("request") == "Variants":
        if not session.get("name"):
            abort(404)
        if type(request.get_json().get("quantity")) == int:
            session["quantity"] = request.get_json().get("quantity")
        else:
            session["quantity"] = 1
        if request.get_json().get("frame") in images[session["name"]]:
            session["frame"] = request.get_json().get("frame")
        else:
            session["frame"] = list(images["Grapes"])[3]
        if request.get_json().get("size") in images[session["name"]][session["frame"]]:
            session["size"] = request.get_json().get("size")
        else:
            session["size"] = list(list(images["Grapes"].values())[3])[0]

        output = (math.ceil((images[session["name"]]
                       [session["frame"]][session["size"]] * curr) * 100)/100)
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
        success_url=url_for("thanks", _external=True, auth="f3423rnjkr3o"),
        cancel_url=url_for("gallery",  _external=True),
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
        curr = get_rate('INR', currency)
        try:
            return render_template("picture.html", images=images[photo], name=photo, currency=curr, symbol=f[currency]["symbol"])
        except:
            abort(404)


@app.route("/thankyou/")
def thanks():
    if request.args.get("auth") == "f3423rnjkr3o":
        return render_template("Thanks.jinja")
    else:
        abort(404)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.jinja'), 404


@app.errorhandler(405)
def page_not_found(e):
    return render_template('404.jinja'), 405


if __name__ == "__main__":
    app.run(debug=True)
