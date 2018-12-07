# project/nifi/forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, SelectField
from wtforms.validators import DataRequired
from flask_wtf.file import FileField, FileAllowed, FileRequired
from werkzeug.utils import secure_filename
from project import nifi

class AddNifiForm(FlaskForm):
    upload = FileField('Local File', validators=[FileRequired()])
    model = SelectField(u'Model (default is ende)', choices=[('ende', 'ende - English to German'), ('kor', 'kor - Korean to English')])
