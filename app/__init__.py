"""
Setup flask app
"""
# pylint: disable=C0103,C0413
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'
login.login_message = "Please, login to see this page"
bootstrap = Bootstrap(app)

from app import routes, models, errors, admin_config

modified_admin = admin_config.MyAdmin()
