from flask.ext.wtf import Form
from wtforms.fields import StringField, PasswordField, SelectField, TextAreaField, FileField
from wtforms.validators import DataRequired, Email, ValidationError
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


class AddTemplateForm(Form):
    name = StringField('Name', validators=[DataRequired(message='Name is required.')])
    price = StringField('Price', validators=[DataRequired(message='Price is required.'), validate_price])
    category = SelectField('Category', coerce=int, validators=[DataRequired(message='Category is required.')])
    description = TextAreaField('Description')
    preview = FileField('Image Preview', validators=[validate_preview])
    files = FileField('Files (Zip)', validators=[DataRequired(message='Files are required.'), validate_files])


