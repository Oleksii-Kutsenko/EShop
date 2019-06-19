"""
Model for flask app
"""
# pylint: disable=E1101
import datetime

from flask_login import UserMixin
from sqlalchemy.orm import load_only
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login


class User(UserMixin, db.Model):
    """
    The user model that extends UserMixin model
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    is_admin = db.Column(db.Boolean, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    last_seen = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    order = db.relationship("Order", back_populates="user")

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
        return '<User {0} email: {1}>'.format(self.username, self.email)


ASSOCIATION_TABLE = db.Table('association', db.Model.metadata,
                             db.Column('order_id', db.Integer, db.ForeignKey('order.id')),
                             db.Column('place_id', db.Integer, db.ForeignKey('place.id'))
                             )


class Order(db.Model):
    """
    The model that contains user order
    """
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship("User", back_populates='order')
    status_id = db.Column(db.Integer, db.ForeignKey('order_status.id'), nullable=False)
    status = db.relationship("OrderStatus", back_populates="children")
    place_id = db.relationship('Place', secondary=ASSOCIATION_TABLE, back_populates="order_id")


class OrderStatus(db.Model):
    """
    The model-dictionary that contains order status
    """
    id = db.Column(db.Integer, primary_key=True)
    order_status_name = db.Column(db.String, nullable=False)
    children = db.relationship("Order", back_populates="status")

    def __repr__(self):
        return str(self.order_status_name)


class Place(db.Model):
    """
    The model that displays information about place on stock
    """
    id = db.Column(db.Integer, primary_key=True)
    taking_date = db.Column(db.DateTime, nullable=False)
    release_date = db.Column(db.DateTime, nullable=False)
    place_type_id = db.Column(db.Integer, db.ForeignKey('place_type.id'), nullable=False)
    place_type = db.relationship("PlaceType", back_populates="places")
    order_id = db.relationship('Order', secondary=ASSOCIATION_TABLE, back_populates="place_id")
    place_class = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float)

    def __repr__(self):
        return "Stock №{0}," \
               " type: {1}," \
               " box-type: {2}," \
               " price: {3}".format(self.id,
                                    PlaceType.query.filter_by(id=self.place_type_id).options(
                                        load_only("place_type_name")).first(),
                                    self.place_class,
                                    self.price)


class PlaceType(db.Model):
    """
    The model that display dictionary of place types
    """
    id = db.Column(db.Integer, primary_key=True)
    place_type_name = db.Column(db.String(50), unique=True, nullable=False)
    places = db.relationship("Place", back_populates='place_type')

    def __repr__(self):
        return "<{}>".format(self.place_type_name)


@login.user_loader
def load_user(user_id):
    """
    This function helps flask_login load a user
    """
    return User.query.get(int(user_id))
