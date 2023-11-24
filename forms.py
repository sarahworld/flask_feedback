from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, PasswordField
from wtforms.validators import InputRequired

class RegisterForm(FlaskForm):

    username = StringField("username");

    password = PasswordField("password")
    
    email = StringField("E-mail")

    first_name = StringField("first_name")
    
    last_name = StringField("last_name")


class LoginForm(FlaskForm):

    username = StringField("username");

    password = PasswordField("password")

class FeedbackForm(FlaskForm):

    title = StringField("Title");

    content = StringField("Content");





    