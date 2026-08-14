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
        if not session:
            session["profile"] = {}
            session["login"] = False
            session["chat"] = {}
            session["profileImage"] = "/static/image/user/anon.png"
            return False
        return session.get("login", False)

    def createAccount(self, new_profile_data):
        session["login"] = True
        session["profile"] = new_profile_data
        if "chats" not in session["profile"]:
            session["profile"]["chats"] = []

    def logoutAccount(self):
        session.clear()

    def updateChatInIndex(self):
        if not session.get("login", False):
            return
        
        username = session["profile"].get("username")
        if not username:
            return
        
        user_chats = Chats.query.filter(
            Chats.participants.contains(username)
        ).all()
        
        updated_chats = []
        for chat in user_chats:
            other_user = [p for p in chat.participants if p != username][0] if chat.participants else None
            
            if other_user:
                updated_chats.append({
                    "chatname": chat.chatname,
                    "participants": chat.participants,
                    "messages_count": len(chat.get_messages())
                })
        
        session["profile"]["chats"] = updated_chats
        
        try:
            user = User.query.filter_by(username=username).first()
            if user:
                pass
        except Exception as e:
            print(f"Error updating user chats: {e}")

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
    participants = db.Column(db.JSON)
    messages = db.Column(db.JSON, default=list)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    
    def add_message(self, sender, message, timestamp=None):
        if self.messages is None:
            self.messages = []
        if timestamp is None:
            timestamp = time.time()
        self.messages.append({
            "sender": sender,
            "message": message,
            "timestamp": timestamp
        })
        db.session.commit()
    
    def get_messages(self):
        return self.messages or []

    def get_participants(self):
        return self.participants or []

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
        extension.updateChatInIndex()
        return render_template("index.html", session=session)

# api
@app.route("/user-exist")
def user_exist():
    username = request.args.get("username")
    email = request.args.get("email")
    password = request.args.get("password")

    if not username or not email or not password:
        return jsonify({
            "login": False,
            "error": "missing_data"
        })

    user = User.query.filter_by(
        username=username,
        email=email,
        password=password
    ).first()

    if user:
        extension.createAccount({
            "username": user.username,
            "email": user.email,
            "chats": []
        })

        return jsonify({
            "login": True
        })

    return jsonify({
        "login": False
    })

@app.route("/auth", methods=["POST"])
def auth():
    username = request.form.get("username")
    email = request.form.get("email")
    password = request.form.get("password")
    confirm_password = request.form.get("confirmPassword")

    if not username or not email or not password:
        flash("لطفاً تمامی فیلدها را پر کنید.")
        return redirect("/")

    user = User.query.filter_by(
        username=username,
        email=email,
        password=password
    ).first()

    if user:
        extension.createAccount({
            "username": user.username,
            "email": user.email,
            "chats": []
        })

        return redirect("/")

    existing_user = User.query.filter(
        (User.username == username) |
        (User.email == email)
    ).first()

    if existing_user:
        flash("نام کاربری یا ایمیل قبلاً استفاده شده است.")
        return redirect("/")

    if not confirm_password:
        flash("تکرار رمز عبور الزامی است.")
        return redirect("/")

    if password != confirm_password:
        flash("رمز عبور و تکرار آن یکسان نیستند.")
        return redirect("/")

    user = User(
        username=username,
        email=email,
        password=password
    )

    db.session.add(user)
    db.session.commit()

    extension.createAccount({
        "username": user.username,
        "email": user.email,
        "chats": []
    })

    return redirect("/")

@app.route("/logout")
def logout():
    global session
    session.clear()
    return redirect("/")

@app.route("/add-contact", methods=["POST"])
def add_contact():
    if not session.get("login", False):
        flash("لطفاً ابتدا وارد شوید.")
        return redirect("/")
    
    user_id = session["profile"].get("username")
    target_id = request.form.get("id")
    
    if not target_id:
        flash("آیدی مخاطب را وارد کنید.")
        return redirect("/")
    
    if user_id == target_id:
        flash("نمی‌توانید خودتان را اضافه کنید.")
        return redirect("/")
    
    target_user = User.query.filter_by(username=target_id).first()
    if not target_user:
        flash("کاربر مورد نظر وجود ندارد.")
        return redirect("/")
    
    chat_name = f"{min(user_id, target_id)}_{max(user_id, target_id)}"
    
    existing_chat = Chats.query.filter_by(chatname=chat_name).first()
    if existing_chat:
        flash("این مخاطب قبلاً اضافه شده است.")
        return redirect("/")

    new_chat = Chats(chatname=chat_name, participants=[user_id, target_id], messages=[])
    
    try:
        db.session.add(new_chat)
        db.session.commit()
        
        if "chats" not in session["profile"]:
            session["profile"]["chats"] = []
        
        session["profile"]["chats"].append({
            "chatname": chat_name,
            "participants": [user_id, target_id]
        })
        
        flash(f"مخاطب {target_id} با موفقیت اضافه شد.")
        
    except Exception as e:
        db.session.rollback()
        flash("خطا در اضافه کردن مخاطب.")
        print(f"Error: {e}")
    
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)