from flask.ext.wtf import Form
from wtforms.fields import StringField, PasswordField
from wtforms.validators import DataRequired, Email


class AddUserForm(Form):
    username = StringField('Username', validators=[DataRequired(message='Username is required.')])
    password = PasswordField('Password', validators=[DataRequired('Password is required')])
    first_name = StringField('First Name')
    last_name = StringField('Last Name')
    email = StringField('Email')
    permission = StringField('Permission', default=0)
