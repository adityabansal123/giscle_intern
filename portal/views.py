from flask import Flask, request, session, redirect, url_for, render_template, flash, send_from_directory
from .models import User
from .models import entries
import os

app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "POST":
        target = os.path.join(APP_ROOT, 'cvs/')
        if not os.path.isdir(target):
            os.mkdir(target)
        for upload in request.files.getlist("file"):
            filename = request.form["username"]
            destination = "/".join([target, filename])
            upload.save(destination)
        Name = request.form["name"]
        username = request.form["username"]
        Email = request.form["email"]
        Contact = request.form["contact"] 
        Password = request.form["password"]
        Linkedin = request.form["linkedin"]
        CV = destination

        user = User(username)

        if not user.register(Name, Email, Contact, Password, Linkedin, CV):
            flash("USER EXISTS")
        else:
            flash("SUCCEESFULLY REGISTERED")
            return redirect(url_for("login"))
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = User(username)

        if not user.verify_password(password):
            flash("INVALID LOGIN")
        else:
            flash("SUCCESSFULLY LOGGED IN")
            session["username"] = user.username
            return redirect(url_for("index"))
    return render_template("login.html")

@app.route("/apply", methods=["POST"])
def apply():
    title = request.form["title"]
    skills = request.form["skills"]
    ques = request.form["ques"]

    user = User(session["username"])

    if not title or not skills or not ques:
        flash("Include title, skills and an answer")
    else:
        user.apply(title, skills, ques)
    
    return redirect(url_for("index"))

@app.route("/admin")
def admin():
    results = entries()
    return render_template("entries.html", results=results)

@app.route("/logout")
def logout():
    session.pop("username")
    flash("LOGGED OUT")
    return redirect(url_for("index"))
