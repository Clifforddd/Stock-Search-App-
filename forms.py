#from ast import Pass
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired


class UserForm(FlaskForm):
    username = StringField("Username", validators = [InputRequired()])
    password = PasswordField("Password", validators= [InputRequired()])

class FavoForm(FlaskForm):
    favo = StringField("Favo", validators = [InputRequired()])
    user_id = StringField("user_id", validators = [InputRequired()])