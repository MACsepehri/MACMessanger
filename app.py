from flask import Flask, render_template, redirect, session, request
import assets

app = Flask(__name__)

# routes
@app.route("/")
def index():
    check = assets.check_session(session)
    if not check:
        return render_template("pages/login.html")
    else:
        return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")