import hashlib

from flask import Flask, render_template, request


# create the base application
app = Flask(__name__)


@app.route("/")
def index():
    return "You should look at /sign or /verify"


@app.route("/sign")
def sign():
    if request.args.get("data"):
        digest = hashlib.sha1(request.args["data"]).hexdigest()
        return render_template(
            "sign.html", digest=digest, data=request.args["data"]
        )
    else:
        return render_template("submit_for_signing.html")


@app.route("/verify")
def verify():
    if request.args.get("data") and request.args.get("digest"):
        computed_digest = hashlib.sha1(request.args["data"]).hexdigest()
        if request.args.get("digest") == computed_digest:
            return "Verified"
        else:
            return "Failed verification"
    else:
        return "Must supply data and digest"


if __name__ == "__main__":
    app.run(debug=True)
