from flask import Flask, render_template, redirect, flash, session, request
from flask_sqlalchemy import SQLAlchemy
from extension import Extension
import os

# init of flask
app = Flask(__name__)
app.secret_key = "admin"
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE_PATH = os.path.join(BASE_DIR, "static", "instance", "database", "main", "security", "database.db")
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DATABASE_PATH}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
extension = Extension(session)

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
    global session

    session, loggedIn = extension.checkSession()
    if not loggedIn:
        return render_template("page/login.html", session=session)
    else:
        return render_template("index.html", session=session)

if __name__ == "__main__":
    app.run(debug=True)