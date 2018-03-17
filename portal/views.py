from flask import Flask, request, session, redirect, url_for, render_template, flash, send_from_directory
from .models import User
from flask import Flask, request, session, redirect, url_for, render_template, flash, send_from_directory
from .models import User
from .models import entries
import os
from flask_basicauth import BasicAuth

app = Flask(__name__)

app.config['BASIC_AUTH_USERNAME'] = 'sumanjha'
app.config['BASIC_AUTH_PASSWORD'] = 'ganeshjha'

basic_auth = BasicAuth(app)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

@app.route("/jobapply")
def jobapply():
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
            return redirect(url_for("internships"))
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
        flash("SUCCESSFULLY APPLIED FOR JOB ROLE")
    
    return redirect(url_for("internships"))

@app.route("/admin")
@basic_auth.required
def admin():
    results = entries()
    return render_template("entries.html", results=results)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/problems")
def problems():
    return render_template("problems.html")

@app.route("/internships")
def internships():
    return render_template("positions.html")

@app.route("/events")
def events():
    return render_template("events.html")

@app.route("/partners")
def partners():
    return render_template("partners.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/university")
def university():
    return render_template("university.html")

@app.route("/")
def home():
    return render_template("home.html")

@app.route('/resume/<username>')
def resume(username):
    return send_from_directory(os.path.join(APP_ROOT, 'cvs/'), username)

@app.route("/logout")
def logout():
    session.pop("username")
    flash("LOGGED OUT")
    return redirect(url_for("home"))
