from flask import Flask, render_template, redirect, flash, session, request
from flask_sqlalchemy import SQLAlchemy
import assets
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_DIR = os.path.join(BASE_DIR, "static", "db")
os.makedirs(DB_DIR, exist_ok=True)
DATABASE = os.path.join(DB_DIR, "users.db")

app = Flask(__name__)
app.secret_key = "test"
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DATABASE}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# define database
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    chats = db.Column(db.JSON)

with app.app_context():
    db.create_all()

# routes
@app.route("/")
def index():
    check = assets.check_session(session)
    if not check:
        return render_template("pages/login.html")
    else:
        return render_template("index.html")

@app.route("/auth", methods=["POST"])
def auth():

    username = request.form.get("username", "")
    password = request.form.get("password", "")
    confirm_password = request.form.get("confirm-password", "")

    if not username or not password or not confirm_password:
        flash(":) Nice Try")
        return redirect("/login")

    if password != confirm_password:
        flash("Passwords are not same.")
        return redirect("/login")

    existing_user = Users.query.filter_by(name=username).first()

    if existing_user:

        if existing_user.password == password:

            session["login"] = True
            session["profile"] = {
                "id": existing_user.id,
                "username": existing_user.name,
                "password": existing_user.password,
                "chats": existing_user.chats
            }

            flash("You have successfuly logged in!")
            return redirect("/")

        flash("Username already exists or password is incorrect.")
        return redirect("/login")

    user = Users(
        name=username,
        password=password,
        chats={"chats": []}
    )

    db.session.add(user)
    db.session.commit()

    session["login"] = True
    session["profile"] = {
        "id": user.id,
        "username": user.name,
        "password": user.password,
        "chats": user.chats
    }

    flash("You have successfuly registered!")
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")