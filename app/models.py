"""
Model for flask app
"""
# pylint: disable=E1101
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
    password_hash = db.Column(db.String(128))

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


@login.user_loader
def load_user(user_id):
    """
    This function helps flask_login load a user
    """
    return User.query.get(int(user_id))
