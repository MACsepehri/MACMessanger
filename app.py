from flask import Flask, render_template, redirect, flash, jsonify, session, request
from flask_sqlalchemy import SQLAlchemy
from deep_translator import GoogleTranslator
import os
import time

# init of flask
app = Flask(__name__)
app.secret_key = "admin"
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE_PATH = os.path.join(BASE_DIR, "static", "instance", "database", "main", "security", "database.db")
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DATABASE_PATH}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class Extension:
    def checkSession(self):
        result = None
        if not session:
            session["profile"] = {}
            session["login"] = False
            session["chat"] = {}
            session["profileImage"] = "/static/image/user/anon.png"
            result = False
        elif not session["login"]:
            result = False
        else:
            result = True
        return result

    def createAccount(self, new_profile_data):
        session["login"] = True
        session["profile"] = new_profile_data

    def logoutAccount(self):
        session.clear()

    def updateChatInIndex(self):
        for data in Chats.query.all():
            pass

extension = Extension()

# database
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, unique=True, nullable=False)

class Chats(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    chatname = db.Column(db.String, unique=True, nullable=False)
    data = db.Column(db.JSON)

# database init
with app.app_context():
    db.create_all()

# routes
@app.route("/")
def index():
    loggedIn = extension.checkSession()
    if not loggedIn:
        return render_template("page/login.html", session=session)
    else:
        return render_template("index.html", session=session)

# api
@app.route("/user-exist")
def user_exist():
    username = request.args.get("username")
    email = request.args.get("email")
    password = request.args.get("password")

    user = User.query.filter((User.username == username) | (User.email == email) | (User.password == password)).first()

    if user.username == username and user.email == email and user.password == password:
        return jsonify({
            "exists": False
        })

    return jsonify({
        "exists": False,
        "user": None
    })

@app.route("/auth", methods=["POST"])
def auth():
    username = request.form.get("username", None)
    email = request.form.get("email", None)
    password = request.form.get("password", None)
    confirm_password = request.form.get("confirmPassword", None)

    user = User.query.filter((User.username == username) | (User.email == email) | (User.password == password)).first()

    if user.username != username or user.email != email or user.password != password:
        flash("تلاش خوبی بود :)")
        return redirect("/")
    elif user.username == username or user.email == email or user.password == password:
        extension.createAccount({
            "username": username,
            "password": password,
            "email": email,
            "chats": []
        })
        return redirect("/")
    if password != confirm_password:
        flash("تلاش خوبی بود :)")
        return redirect("/")
    elif username == None or email == None or password == None or confirm_password == None:
        flash("تلاش خوبی بود :)")
        return redirect("/")

    user = User(username=username, email=email, password=password)
    extension.createAccount({
        "username": username,
        "password": password,
        "email": email,
        "chats": []
    })
    db.session.add(user)
    db.session.commit()
    return redirect("/")

@app.route("/logout")
def logout():
    global session
    session.clear()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)