from flask import Flask, redirect, render_template, url_for, request
import yaml

with open("db.yaml", "r") as y:
    db = yaml.load(y)

valid = {
    "Haze": "2,500",
    "bridge": 50,
    "something": 0.1,
    "shivansh": 1000
}

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/Gallery/")
def gallery():
    return render_template("photos.jinja", images=db["images"])


@app.route("/Gallery/<photo>/")
def product(photo):
    try:
        return render_template("picture.jinja", images=db["images"][photo], name=photo)
    except:
        return render_template("404.jinja")

if __name__ == "__main__":
    app.run(debug=True)
