from flask.ext.wtf import Form
from wtforms.fields import StringField, HiddenField, SelectField, FloatField, TextAreaField, FileField, IntegerField
from wtforms.validators import DataRequired, ValidationError, NumberRange
from werkzeug.utils import secure_filename


ALLOWED_PREVIEW_EXTENSIONS = ['png', 'jpg', 'jpeg']
ALLOWED_FILES = ['zip']


def allowed_preview_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_PREVIEW_EXTENSIONS


def allowed_files(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_FILES


def validate_preview(self, field):
    field.data.filename = secure_filename(field.data.filename)
    if not allowed_preview_file(field.data.filename):
        raise ValidationError('Image preview must be a .png, .jpg, or .jpeg')


def validate_files(self, field):
    field.data.filename = secure_filename(field.data.filename)
    if not allowed_files(field.data.filename):
        raise ValidationError('Files must be a .zip')


def validate_price(self, field):
    try:
        field.data = "{:.2f}".format(float(field.data))
    except:
        raise ValidationError('Price must be a number.')

def duration_choices():
    choices = []
    for i in range(1, 8):
        choices.append((i, str(i) + ' days'))
    return choices

class AddTemplateForm(Form):
    name = StringField('Name', validators=[DataRequired(message='Name is required.')])
    price = FloatField('Price', validators=[NumberRange(min=1, message='Price must be greater than 0.'), DataRequired(message='Price is required.'), validate_price])
    category = SelectField('Category', coerce=int, validators=[DataRequired(message='Category is required.')])
    description = TextAreaField('Description')
    preview = FileField('Image Preview', validators=[validate_preview])
    files = FileField('Files (Zip)', validators=[DataRequired(message='Files are required.'), validate_files])
    tags = HiddenField()
    custom_tags = HiddenField()

class AddServiceForm(Form):
    name = StringField('Name', validators=[DataRequired(message='Name is required.')])
    start_price = StringField('Start Price', validators=[DataRequired(message='Start price is required.'), validate_price])
    description = TextAreaField('Description', validators=[DataRequired(message='Description is required.')])
    #end_date = DateTimeField('End date', format='%m/%d/%Y %I:%M %p', validators=[DataRequired(message='End date is required.')])
    duration = SelectField('Duration', choices=duration_choices(), coerce=int, validators=[DataRequired(message='Duration required')])
