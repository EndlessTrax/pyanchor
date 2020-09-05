from flask import Flask, render_template


app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("success.html", name="About")


@app.route("/contact")
def contact():
    return render_template("success.html", name="Contact")


@app.route("/login")
def login():
    return render_template("error.html", status_code=401), 401


@app.route("/500")
def five_hundred():
    return render_template("error.html", status_code=500), 500


@app.route("/sitemap.xml")
def sitemap():
    return render_template('sitemap.xml')


if __name__ == "__main__":
    app.run()
