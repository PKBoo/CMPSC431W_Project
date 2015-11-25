from flask.ext.wtf import Form
from wtforms.fields import StringField, PasswordField, SelectField
from wtforms.validators import DataRequired, Email
import datetime

def month_choices():
    choices = []
    for i in range(1, 13):
        choices.append((i,i))

    return choices

def year_choices():
    choices = []
    now = datetime.datetime.now()
    current_year = now.year

    for i in range(current_year, current_year + 11):
        choices.append((i,i))
    return choices

class PaymentInformationForm(Form):
    name = StringField('Name on Card', validators=[DataRequired(message='Name on card is required.')])
    number = StringField('Card Number', validators=[DataRequired('Card number is required.')])
    expiration = StringField('Expiration', validators=[DataRequired('Expiration date is required.')])

    expiration_month = SelectField('Month', choices=month_choices())
    expiration_year = SelectField('Year', choices=year_choices())

    cvc = StringField('CVC/CW', validators=[DataRequired('Security code is required.')])

