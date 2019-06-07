"""
Model for flask app
"""
# pylint: disable=E1101
import datetime

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login


class User(UserMixin, db.Model):
    """
    The user model that extends UserMixin model
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    is_admin = db.Column(db.Boolean)
    password_hash = db.Column(db.String(128))
    last_seen = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def set_password(self, password):
        """
        Set password for a user model
        """
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """
        Check passwords hashes when user tries to log in
        """
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        """
        Return a string representation of the model
        """
        return '<User {}>'.format(self.username)


class Order(db.Model):
    """
    The model that contains user order
    """
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    place_id = db.Column(db.Integer, db.ForeignKey('place.id'))


class PlaceType(db.Model):
    """
    The model that display dictionary of place types
    """
    id = db.Column(db.Integer, primary_key=True)
    place_type_name = db.Column(db.String(50), unique=True)


class Place(db.Model):
    """
    The model that displays information about place on stock
    """
    id = db.Column(db.Integer, primary_key=True)
    taking_date = db.Column(db.DateTime)
    release_date = db.Column(db.DateTime)
    place_type = db.Column(db.Integer, db.ForeignKey('place_type.id'))
    square = db.Column(db.Float)
    price = db.Column(db.Float)


@login.user_loader
def load_user(user_id):
    """
    This function helps flask_login load a user
    """
    return User.query.get(int(user_id))
