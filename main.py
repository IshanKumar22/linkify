import hashlib
from flask import Flask, render_template, request, redirect

app = Flask(__name__)
app.config["SECRET_KEY"] = "ae93ec19909d56777c37c55dd9be07ab"
urls = {}


@app.route("/")
def index():
    """
        Renders the index.html file
    """
    return render_template("index.html")


@app.route("/shorten_url", methods=["POST"])
def shorten_url():
    """
        Takes the long url, shortens it, saves it to the url dictionary and renders the shorten_url.html file
    """
    long_url = request.form["long_url"]
    host_url = request.form["hostname"]
    hashed = hashlib.md5(long_url.encode()).hexdigest()[:8]
    urls[hashed] = long_url
    short_url = host_url + hashed
    return render_template("shorten_url.html", short_url=short_url)


@app.route("/<hashed>")
def redirect_url(hashed: str):
    """
        Redirects the short url to the long url

        :params hashed: The code for the short url
    """
    long_url = urls.get(hashed)
    if long_url:
        return redirect(long_url)
    else:
        return render_template("404.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8081, debug=True)
