import os

from flask import Flask, flash, redirect, render_template, request, url_for
from flask.ext import login
from flask.ext.sqlalchemy import SQLAlchemy


# create the base application
app = Flask(__name__)
# obtain the current directory path
db_path = os.path.join(os.path.abspath(os.path.curdir), "db.sqlite")

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///{0}".format(db_path)
app.secret_key = "iamreallysecret"
# create the DB object
db = SQLAlchemy(app)
# set up the schema
# create a login manager
login_manager = login.LoginManager()
login_manager.init_app(app)
login_manager.login_view = "_login"


class User(db.Model, login.UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), unique=True)
    password = db.Column(db.String(40))

    def __init__(self, username, password):
        self.username = username
        self.password = password


@app.route("/")
@login.login_required
def index():
    return render_template("index.html")


@login_manager.user_loader
def load_user(userid):
    return User.query.get(userid)


@app.route('/logout')
def logout():
    login.logout_user()
    return redirect(url_for('_login'))


@app.route("/login", methods=["GET", "POST"])
def _login():
    if request.method == "GET":
        return render_template("login.html")

    username = request.form["username"]
    password = request.form["password"]

    query = User.query.filter_by(
        username=username,
        password=password
    )

    db_user = query.first()

    if not db_user:
        flash("Username or password is invalid", "error")
        return redirect(url_for("_login"))

    login.login_user(db_user)
    flash("Logged in successfully")
    return redirect(url_for('index'))

if __name__ == "__main__":
    if not os.path.exists(db_path):
        db.create_all()
        admin = User('admin', 'password')
        db.session.add(admin)
        db.session.commit()

    app.run(debug=True)
