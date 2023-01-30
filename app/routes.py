"""
Functions that handle requests at end-point
"""
# pylint: disable=E1101, R0401
import json
from datetime import datetime, timedelta

from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse

from app import app, db
from app.forms import LoginForm, RegistrationForm, ChangePassword, ChangeUsername
from app.models import User, Place, Order


@app.before_request
def before_request():
    """
    Update user last_seen time
    """
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@app.route("/")
@app.route("/index")
def index():
    """
    Return a homepage
    """
    num = {}
    for place_type_id in range(1, 4):
        for place_class in [1, 3, 7, 14, 28]:
            num[str(place_type_id) + ":" + str(place_class)] = (
                Place.query.filter(Place.place_class == place_class)
                .filter(Place.place_type_id == place_type_id)
                .filter(datetime.now() >= Place.release_date)
                .count()
            )
    return render_template("index.html", stock=num)


@app.route("/", methods=["GET", "POST"])
@app.route("/login", methods=["GET", "POST"])
def login():
    """
    This function return a login page
    """
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = LoginForm()
    if form.validate_on_submit():
        logging_user = User.query.filter_by(username=form.username.data).first()
        if logging_user is None or not logging_user.check_password(form.password.data):
            flash("Invalid username or password")
            return redirect(url_for("login"))
        login_user(logging_user, remember=form.remember_me.data)
        next_page = request.args.get("next")
        if not next_page or url_parse(next_page).netloc != "":
            next_page = url_for("index")
        return redirect(next_page)
    return render_template("login.html", title="Sign in", form=form)


@app.route("/logout")
def logout():
    """
    The endpoint that logs out the user
    """
    logout_user()
    return redirect(url_for("login"))


@app.route("/register", methods=["GET", "POST"])
def register():
    """
    This function returns register page
    """
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = RegistrationForm()
    if form.validate_on_submit():
        # noinspection PyArgumentList
        new_user = User(
            username=form.username.data, email=form.email.data, is_admin=False
        )
        new_user.set_password(form.password.data)
        db.session.add(new_user)
        db.session.commit()
        flash("Congratulations, you are now a registered user!")
        return redirect(url_for("login"))
    return render_template("register.html", title="Register", form=form)


@app.route("/user/<username>")
@login_required
def user(username):
    """
    The endpoint that returns profile page
    """
    username = current_user.username if username != current_user.username else username
    user_record = User.query.filter_by(username=username).first_or_404()
    return render_template("user.html", user=user_record)


@app.route("/change_username", methods=["GET", "POST"])
@login_required
def change_username():
    """
    The endpoint that helps the user to change his username
    """
    form = ChangeUsername(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        db.session.commit()
        flash("Your changes have been saved.")
    elif request.method == "GET":
        form.username.data = current_user.username
    else:
        flash("Please use a different name")
    return render_template("change_username.html", title="Change username", form=form)


@app.route("/change_password", methods=["GET", "POST"])
@login_required
def change_password():
    """
    The endpoint that helps the user to change his password
    """
    form = ChangePassword()
    if form.validate_on_submit():
        if current_user.check_password(form.old_password.data):
            current_user.set_password(form.new_password.data)
            db.session.commit()
            flash("Your changes have been saved.")
            return redirect(url_for("change_password"))
        flash("Old password isn't valid")
        return redirect(url_for("change_password"))
    return render_template(
        "change_password.html", title="Edit Password", form=ChangePassword()
    )


@app.route("/505", methods=["GET"])
def internal_error():
    """
    Returns 505 error page
    """
    return render_template("500.html")


@app.route("/cart", methods=["GET"])
def cart():
    """
    Returns cart page
    """
    return render_template("cart.html")


@app.route("/buy", methods=["POST"])
def buy():
    """
    The endpoint that responses for make Order and changes place taking and release date
    """
    session_storage = json.loads(request.data)
    basket = json.loads(session_storage["basket"])
    new_order = Order(user_id=current_user.id, status_id=1)
    for item in basket:
        number = basket[item]
        items = item.split(":")
        query = (
            Place.query.filter(Place.place_type_id == items[0])
            .filter(Place.place_class == items[2])
            .filter(Place.release_date < datetime.now())
        )
        if query.count() >= number:
            for place in query.all():
                if basket[item] == 0:
                    break
                new_order.place_id.append(place)
                place.taking_date = datetime.now()
                place.release_date = place.taking_date + timedelta(32)
                db.session.add(new_order)
                basket[item] -= 1
        else:
            return 500

        db.session.commit()

    return "", 200
