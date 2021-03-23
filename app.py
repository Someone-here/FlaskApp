from flask import Flask, redirect, render_template, url_for, request, jsonify
import yaml

with open("db.yaml", "r") as y:
    db = yaml.load(y, yaml.FullLoader)

images = db["images"]

app = Flask(__name__)

types = []
types.append("All")
for i in images:
    if not images[i]["type"] in types:
        types.append(images[i]["type"])
        print(types)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/ip")
def get_my_ip():
    return request.environ.get('HTTP_X_REAL_IP', request.remote_addr)


@app.route("/Gallery/")
def gallery():
    return render_template("photos.html", images=images, types=types)


@app.route("/Gallery/<photo>/")
def product(photo):
    try:
        return render_template("picture.jinja", images=images[photo], name=photo)
    except:
        return render_template("404.jinja")


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.jinja'), 404


if __name__ == "__main__":
    app.run(debug=True)
