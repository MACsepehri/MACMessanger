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


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    chats = db.Column(db.JSON, default=lambda: {"chats": []})


with app.app_context():
    db.create_all()


def sync_contacts(user):
    """
    If another user already has `user` in their contacts,
    add that other user to `user`'s contacts as well.
    """

    all_users = Users.query.all()

    user_chats = user.chats or {"chats": []}
    user_chats_list = user_chats.get("chats", [])

    changed = False

    for other_user in all_users:

        # Don't compare the user with themselves
        if other_user.id == user.id:
            continue

        other_chats = other_user.chats or {"chats": []}

        # Check if other_user has current user
        found = any(
            chat.get("id") == user.id
            for chat in other_chats.get("chats", [])
        )

        if not found:
            continue

        # Check if current user already has other_user
        already_exists = any(
            chat.get("id") == other_user.id
            for chat in user_chats_list
        )

        if already_exists:
            continue

        # Add other_user to current user's contacts
        user_chats_list.append({
            "id": other_user.id,
            "username": other_user.name,
            "messages": []
        })

        changed = True

    if changed:
        user.chats = {
            "chats": user_chats_list
        }

        db.session.commit()


@app.route("/")
def index():

    if not assets.check_session(session):
        return render_template("pages/login.html")

    user = db.session.get(Users, session["user_id"])

    if user is None:
        session.clear()
        return redirect("/")

    sync_contacts(user)

    return render_template(
        "index.html",
        user=user
    )


@app.route("/auth", methods=["POST"])
def auth():

    username = request.form.get("username", "").strip()
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

            session.clear()

            session["login"] = True
            session["user_id"] = existing_user.id

            flash("You have successfully logged in!")

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

    session.clear()

    session["login"] = True
    session["user_id"] = user.id

    flash("You have successfully registered!")

    return redirect("/")


@app.route("/logout")
def logout():

    session.clear()

    return redirect("/")


@app.route("/add-contact", methods=["POST"])
def add_contact():

    if not assets.check_session(session):
        return redirect("/")

    publicID = request.form.get("publicID", "").strip()

    try:
        publicID = int(publicID)

    except (TypeError, ValueError):
        flash("Invalid Public ID.")
        return redirect("/")

    current_user = db.session.get(
        Users,
        session["user_id"]
    )

    target_user = db.session.get(
        Users,
        publicID
    )

    if current_user is None:
        session.clear()
        return redirect("/")

    if target_user is None:
        flash("User not found.")
        return redirect("/")

    if current_user.id == target_user.id:
        flash("You can't add yourself.")
        return redirect("/")

    old_chats = current_user.chats or {"chats": []}
    chats = {"chats": list(old_chats.get("chats", []))}

    if any(chat.get("id") == target_user.id for chat in chats["chats"]):
        flash("This user is already in your contacts.")
        return redirect("/")

    chats["chats"].append({
        "id": target_user.id,
        "username": target_user.name,
        "messages": []
    })
    current_user.chats = chats


    old_target_chats = target_user.chats or {"chats": []}
    target_chats = {"chats": list(old_target_chats.get("chats", []))}

    if not any(chat.get("id") == current_user.id for chat in target_chats["chats"]):
        target_chats["chats"].append({
            "id": current_user.id,
            "username": current_user.name,
            "messages": []
        })
        target_user.chats = target_chats


    db.session.commit()

    flash("Contact added successfully!")

    return redirect("/")



if __name__ == "__main__":
    app.run(
        debug=True,
        host="0.0.0.0"
    )