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
    return render_template("photos.html")


@app.route("/Gallery/<photo>/")
def product(photo):
    if photo in valid:
        return render_template("picture.j2", name=photo, price=db["photography"]["flora"]["Grapes"]["price"]["cm100"], image=db["photography"]["flora"]["Grapes"]["path"], potrait=db["photography"]["flora"]["Grapes"]["potrait"], cm150=db["photography"]["flora"]["Grapes"]["price"]["cm150"], cm200=db["photography"]["flora"]["Grapes"]["price"]["cm200"])
    else:
        return f"<h1>404</h1> \n {photo} was not found"


app.run(debug=True)
