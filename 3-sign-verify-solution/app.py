import hashlib
import hmac

from flask import Flask, render_template, request


# create the base application
app = Flask(__name__)

KEY = b"my_hmac_key"


@app.route("/")
def index():
    return "You should look at /sign or /verify"


@app.route("/sign")
def sign():
    if request.args.get("data"):
        ctx = hmac.new(KEY, digestmod=hashlib.sha256)
        ctx.update(request.args["data"])
        digest = ctx.hexdigest()
        return render_template(
            "sign.html", digest=digest, data=request.args["data"]
        )
    else:
        return render_template("submit_for_signing.html")


@app.route("/verify")
def verify():
    if request.args.get("data") and request.args.get("digest"):
        ctx = hmac.new(KEY, digestmod=hashlib.sha256)
        ctx.update(request.args["data"])
        computed_digest = ctx.hexdigest().decode('utf8')
        if hmac.compare_digest(request.args["digest"], computed_digest):
            return "Verified"
        else:
            return "Failed verification"
    else:
        return "Must supply data and digest"


if __name__ == "__main__":
    app.run(debug=True)
