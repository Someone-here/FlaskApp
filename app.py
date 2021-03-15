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
        return render_template("picture.jinja", name=photo, price=db["images"][photo]["cm100"], image=db["images"][photo]["path"], potrait=db["images"][photo]["potrait"], cm150=db["images"][photo]["cm150"], cm200=db["images"][photo]["cm200"])
    except:
        return f"<h1>404</h1> \n {photo} was not found"


if __name__ == "__main__":
    app.run(debug=True)
