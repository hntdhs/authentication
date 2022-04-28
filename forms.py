from ast import Str
import email
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Length, NumberRange, Email, Optional
from flask_wtf import FlaskForm

class LoginForm(FlaskForm):
    """form for logging in a registered user"""

    username = StringField(
        "Username",
        validators=[InputRequired(), Length(min=5, max=25)],
    )

    password = PasswordField(
        "password",
        validators=[InputRequired(), Length(min=6, max=25)],
    )

class RegisterForm(FlaskForm):
    """form for registering a user"""

    username = StringField(
        "username",
        validators=[InputRequired(), Length(min=5, max=25)],    
    )

    password = PasswordField(
        "password",
        validators=[InputRequired(), Length(min=6, max=25)],
    )

    email = StringField(
        "email",
        validators=[InputRequired(), Email(), Length(max=50)],
    )

    first_name = StringField(
        "first name",
        validators=[InputRequired(), Length(max=30)],
    )

    last_name = StringField(
        "last name",
        validators=[InputRequired(), Length(max=30)],
    )

class FeedbackForm(FlaskForm):
    """form for a user to submit feedback"""

    title = StringField(
        "title",
        validators=[InputRequired(), Length(max=100)],
    )
    content = StringField(
        "content",
        validators=[InputRequired()],
    )

class DeleteForm(FlaskForm):
    """delete form - intentionally left blank?"""
    # why is this blank?