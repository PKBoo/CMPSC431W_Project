from flask.ext.wtf import Form
from wtforms.fields import StringField, PasswordField
from wtforms.validators import DataRequired, Email


class PaymentInformationForm(Form):
    name = StringField('Name on Card', validators=[DataRequired(message='Name on card is required.')])
    number = StringField('Card Number', validators=[DataRequired('Card number is required.')])
    expiration = StringField('Expiration', validators=[DataRequired('Expiration date is required.')])
    cvc = StringField('CVC/CW', validators=[DataRequired('Security code is required.')])
