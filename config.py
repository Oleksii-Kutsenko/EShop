"""
Configuration file for flask app
"""
import os


# pylint: disable=R0903
class Config():
    """
    Configuration class; imports to __init__.py
    """
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
