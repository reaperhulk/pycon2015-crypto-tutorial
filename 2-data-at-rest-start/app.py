import os

from flask import (
    Flask, Response, flash, redirect, render_template, request, url_for
)
from flask.ext import login
from flask.ext.sqlalchemy import SQLAlchemy

from sqlalchemy_utils.types.password import PasswordType


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
    password = db.Column(PasswordType(
        schemes=[
            'bcrypt',
            'plaintext'
        ],
        deprecated=['plaintext'],
        max_length=40
    ))

    def __init__(self, username, password):
        self.username = username
        self.password = password


class EncryptedFile(db.Model):
    def __init__(self, user_id, payload, file_name, mime_type):
        self.user_id = user_id
        self.payload = payload
        self.file_name = file_name
        self.mime_type = mime_type

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), index=True)
    payload = db.Column(db.LargeBinary)
    file_name = db.Column(db.String(255))
    mime_type = db.Column(db.String(255))


@app.route("/")
@login.login_required
def index():
    return render_template("index.html")


@app.route("/download/<file_id>")
@login.login_required
def download(file_id):
    query = EncryptedFile.query.filter_by(
        id=file_id,
        user_id=login.current_user.id,
    )
    result = query.first()
    if not result:
        return "Invalid"
    else:
        resp = Response(
            result.payload,
            status=200,
            mimetype=result.mime_type
        )
        resp.headers["Content-Disposition"] = (
            'attachment; filename="{0}"'.format(result.file_name)
        )
        return resp


@app.route("/upload", methods=["POST"])
@login.login_required
def upload():
    file = request.files['file_data']
    if file:
        ef = EncryptedFile(
            login.current_user.id,
            file.stream.read(),
            file.filename,
            file.mimetype
        )
        db.session.add(ef)
        db.session.commit()
        return "Saved. <a href='/download/{0}'>Download here</a>".format(ef.id)


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

    query = User.query.filter_by(username=username)

    db_user = query.first()

    if not db_user or not _verify_password(db_user, password):
        flash("Username or password is invalid", "error")
        return redirect(url_for("_login"))

    login.login_user(db_user)
    flash("Logged in successfully")
    return redirect(url_for('index'))


def _verify_password(db_user, password):
    if db_user.password == password:
        # ideally we don't save this unless it has changed
        db.session.add(db_user)
        db.session.commit()
        return True
    else:
        return False

if __name__ == "__main__":
    if not os.path.exists(db_path):
        db.create_all()
        admin = User('admin', 'password')
        db.session.add(admin)
        db.session.commit()

    app.run(debug=True)
