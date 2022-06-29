# from crypt import methods
# from nis import cat
from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user
from flask import send_from_directory

auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash("Logged in successfully!", category="success")
                login_user(user, remember=True)
                return redirect(url_for("views.home"))
            else:
                flash("incorrect password, try again.", category="error")
        else:
            flash("Email does not exist.", category="error")
    return render_template("login.html", user=current_user)


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))


@auth.route("/about", methods=["GET", "POST"])
def about():
    return render_template("about.html", user=current_user)


@auth.route("/faq", methods=["GET", "POST"])
def faq():
    return render_template("faq.html", user=current_user)


@auth.route("/sign-up", methods=["GET", "POST"])
def sign_up():
    if request.method == "POST":
        email = request.form.get("email")
        firstName = request.form.get("firstName")
        lastName = request.form.get("lastName")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        user = User.query.filter_by(email=email).first()
        if user:
            flash("Email already exists.", category="error")
        elif len(email) < 4:
            flash("Email must be greater than 3 characetrs", category="error")
        elif len(firstName) < 2:
            flash(" First name must be greater than 4 characetrs", category="error")
        elif len(lastName) < 2:
            flash(" last name must be greater than 4 characetrs", category="error")
        elif password1 != password2:
            flash("passwords don't match", category="error")
        elif len(password1) < 7:
            flash("password must be at least 7 characetrs", category="error")
        else:
            new_user = User(
                email=email,
                firstName=firstName,
                password=generate_password_hash(password1),
            )
            db.session.add(new_user)
            db.session.commit()
            login_user(user, remember=True)
            flash("account created!", category="success")
            return redirect(url_for("views.home"))

    return render_template("signup.html", user=current_user)
