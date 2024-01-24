from flask import Flask, render_template, request, redirect, url_for, make_response
import db
import bcrypt
from models import User
import json


app = Flask(__name__)

def reiniciar_bbdd():
    db.Base.metadata.drop_all(db.engine)
    db.Base.metadata.create_all(db.engine)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        password = request.form["password"].encode("utf-8")
        password_hashed = bcrypt.hashpw(password, bcrypt.gensalt())

        register_user = User(
            name = request.form["name"],
            email = request.form["email"],
            password = password_hashed
        )

        db.session.add(register_user)
        db.session.commit()

        return redirect(url_for("home"))

    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login_user():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"].encode("utf-8")

        user = db.session.query(User).filter_by(email=email).first()

        # user_data = {
        #     'id': user.id,
        #     'name': user.name,
        #     'email': user.email
        # }

        if user and bcrypt.checkpw(password, user.password):
            resp = make_response(redirect(url_for("home")))
            # resp.set_cookie('user_data', json.dumps(user_data))
            resp.set_cookie('name', json.dumps(user.name))
            resp.set_cookie('email', json.dumps(user.email))

            return resp
        
        else:
            return "Invalid email or password"
        
    return render_template("login.html")

if __name__ == '__main__':
    reiniciar_bbdd()
    app.run(debug=True)