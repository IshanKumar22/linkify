from flask import Flask, render_template, request, redirect
import hashlib
import ssl

app = Flask(__name__)
app.config["SECRET_KEY"] = "ae93ec19909d56777c37c55dd9be07ab"
urls = {}

context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain("cert.pem", "key.pem")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/shorten_url", methods=["POST"])
def shorten_url():
    long_url = request.form["long_url"]
    hash = hashlib.md5(long_url.encode()).hexdigest()[:8]
    urls[hash] = long_url
    short_url = request.host_url + hash
    return render_template("shorten_url.html", short_url=short_url)

@app.route("/<hash>")
def redirect_url(hash):
    long_url = urls.get(hash)
    if long_url:
        return redirect(long_url)
    else:
        return render_template("404.html")

if __name__ == "__main__":
    app.run(host="192.168.0.108", port=80, debug=True, ssl_context=context)
