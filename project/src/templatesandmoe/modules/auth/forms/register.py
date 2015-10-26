from flask.ext.wtf import Form
from wtforms.fields import StringField, PasswordField
from wtforms.validators import DataRequired, Email


class RegisterForm(Form):
    username = StringField('Username', validators=[DataRequired(message='Username is required.')])
    password = PasswordField('Password', validators=[DataRequired(message='Password is required.')])
    first_name = StringField('First Name')
    last_name = StringField('Last Name')
    email = StringField('Email', validators=[DataRequired(message='Email is required')])
