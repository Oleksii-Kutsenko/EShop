"""
Configuration file for flask app
"""
import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    """
    Configuration class; imports to __init__.py
    """

    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(os.getcwd(), 'db.sqlite3')}"
    SECRET_KEY = os.environ.get("SECRET_KEY")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
