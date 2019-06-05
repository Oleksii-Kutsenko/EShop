from flask_admin.contrib.sqla import ModelView

import app
from app.models import User, PlaceType, Place, Order

app.m_admin.add_view(ModelView(User, app.db.session))
app.m_admin.add_view(ModelView(PlaceType, app.db.session))
app.m_admin.add_view(ModelView(Place, app.db.session))
app.m_admin.add_view(ModelView(Order, app.db.session))
