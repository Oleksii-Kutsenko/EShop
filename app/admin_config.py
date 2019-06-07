"""
The module that configures a flask-admin extension
"""
from flask_admin import AdminIndexView, Admin
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user

from app import app, db
from app.models import User, PlaceType, Place, Order


class ProtectedIndexView(AdminIndexView):
    """
    The class that provides access to admin panel only to admins
    """

    def is_accessible(self):
        """
        The function that checks if the current user is an admin
        """
        if not current_user.is_authenticated:
            return False
        if not current_user.is_admin:
            return False
        return True


class MyAdmin(Admin):
    """
    The admin class that extends standard and add some views to it
    """

    def __init__(self):
        """
        The constructor of the class
        """
        super(MyAdmin, self).__init__(app,
                                      name='app',
                                      template_mode='bootstrap3',
                                      index_view=ProtectedIndexView())
        self.add_view(ModelView(User, db.session))
        self.add_view(ModelView(PlaceType, db.session))
        self.add_view(ModelView(Place, db.session))
        self.add_view(ModelView(Order, db.session))
