from flask.ext.wtf import Form
from wtforms.fields import StringField, PasswordField
from wtforms.validators import DataRequired, Email


class UserForm(Form):
    username = StringField('Username', validators=[DataRequired(message='Username is required.')])
    password = PasswordField('Password')
    first_name = StringField('First Name')
    last_name = StringField('Last Name')
    email = StringField('Email')
    permissions = StringField('Permissions', default=0)
