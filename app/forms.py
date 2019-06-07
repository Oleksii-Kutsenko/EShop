"""
Forms for flask app
"""
# pylint: disable=R0201,E1101
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Email, EqualTo, DataRequired, ValidationError

# pylint: disable=E1101
from app.models import User


class LoginForm(FlaskForm):
    """
    The form that helps to log in a user
    """
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    """
    The form that helps to register a user
    """
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        """
        Raise an error if a username is already taken
        """
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        """
        Raise an error if a email is already taken
        """
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')


class ChangeUsername(FlaskForm):
    """
    The form that helps a user to change his username
    """
    username = StringField('Username', validators=[DataRequired()])
    submit = SubmitField('Save')

    def __init__(self, original_username, *args, **kwargs):
        super(ChangeUsername, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        """
        The function that helps to validate new username
        """
        if username.data != self.original_username:
            user = User.query.filter_by(username=username.data).first()
            if user is not None:
                raise ValidationError('Please use a different username.')


class ChangePassword(FlaskForm):
    """
    The form that helps a user to change his password
    """
    old_password = PasswordField('Old password', validators=[DataRequired()])
    new_password = PasswordField('New password', validators=[DataRequired()])
    repeat_new_password = PasswordField('Repeat new password',
                                        validators=[DataRequired(),
                                                    EqualTo('new_password')])
    submit = SubmitField('Save')
