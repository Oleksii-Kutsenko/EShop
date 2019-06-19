"""
The module that configures a flask-admin extension
"""
from flask_admin import AdminIndexView, Admin, BaseView, expose
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user

from app import app, db
from app.models import User, PlaceType, Place, Order, OrderStatus


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


class OrderModelView(ModelView):
    """
    Class that format Order Model view
    """
    column_display_pk = True


class ExitView(BaseView):
    """
    Class that protect admin panel from other user
    """

    @expose('/')
    def index(self):
        """
        The method that returns admin panel page
        """
        return self.render('admin/panel.html')


class MyAdmin(Admin):
    """
    The admin class that extends standard and add some views to it
    """

    def __init__(self):
        """
        The constructor of the class
        """
        super(MyAdmin, self).__init__(app,
                                      name='Stock',
                                      template_mode='bootstrap3',
                                      index_view=ProtectedIndexView())
        self.add_view(ModelView(User, db.session))
        self.add_view(ModelView(PlaceType, db.session))
        self.add_view(ModelView(Place, db.session))
        self.add_view(OrderModelView(Order, db.session))
        self.add_view(ModelView(OrderStatus, db.session))
        self.add_view(ExitView(name='Exit', endpoint='logout'))
