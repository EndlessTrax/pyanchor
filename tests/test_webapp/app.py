from flask import Flask, render_template


app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/about/")
def about():
    sub_links = ["/link-1", "/link-2"]
    return render_template("success.html", name="About", links=sub_links)


@app.route("/about/link-1")
def about_link_1():
    return render_template("success.html", name="About Link 1")


@app.route("/about/link-2")
def about_link_2():
    return render_template("success.html", name="About Link 2")


@app.route("/contact")
def contact():
    return render_template("success.html", name="Contact")


@app.route("/rel")
def relative_link():
    return render_template("success.html", name="Rel")


@app.route("/rel2")
def relative_link2():
    return render_template("success.html", name="Rel2")


@app.route("/login")
def login():
    return render_template("error.html", status_code=401), 401


@app.route("/500")
def five_hundred():
    return render_template("error.html", status_code=500), 500


@app.route("/sitemap.xml")
def sitemap():
    return render_template("sitemap.xml")


if __name__ == "__main__":
    app.run()
