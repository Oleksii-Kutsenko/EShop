"""
The module that helps handle errors
"""
from flask import render_template

from app import app, db


@app.errorhandler(403)
def forbidden(error):
    """
    Render a page for 403 error
    """
    app.logger.error(error)
    return render_template("403.html"), 403


@app.errorhandler(404)
def not_found_error(error):
    """
    Render a page for 404 error
    """
    app.logger.error(error)
    return render_template("404.html"), 404


@app.errorhandler(500)
def internal_error(error):
    """
    Render a page for 500 error
    """
    app.logger.error(error)
    db.session.rollback()
    return render_template("500.html"), 500
