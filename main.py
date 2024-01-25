from flask import Flask, render_template, request, redirect, url_for, make_response
import db
import bcrypt
import json
import os
import jwt

from models import User, Token
from dotenv import load_dotenv


app = Flask(__name__)

load_dotenv()
jwt_secret = os.getenv("JWT_SECRET")

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

        if user and bcrypt.checkpw(password, user.password):
            user_data = {
                'id': user.id,
                'name': user.name,
                'email': user.email
            }

            token = jwt.encode(user_data, os.getenv('JWT_SECRET'), algorithm='HS256')

            new_token = Token(user_id=user.id, token=token)
            db.session.add(new_token)
            db.session.commit()

            decoded_data = jwt.decode(token, os.getenv('JWT_SECRET'), algorithms=['HS256'])
            print(decoded_data)

            resp = make_response(redirect(url_for("home")))
            resp.set_cookie('token', token)
            return resp
        
        else:
            return "Invalid email or password"
        
    return render_template("login.html")






if __name__ == '__main__':
    reiniciar_bbdd()
    app.run(debug=True)