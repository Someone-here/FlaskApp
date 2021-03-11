from flask import Flask, redirect, render_template, url_for, request

valid = {
    "Haze": 100,
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
        return render_template("picture.html", name=photo, price=valid[photo])
    else:
        return f"<h1>404</h1> \n {photo} was not found"

app.run(debug=True)