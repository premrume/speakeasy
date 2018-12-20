# project/nifi/forms.py

from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField
from flask_wtf.file import FileField, FileAllowed, FileRequired

class AddNifiForm(FlaskForm):
    upload = FileField(
      u'Choose 1 to 5 Files (jpg, png, txt)', 
      validators=[
        FileRequired(),
        FileAllowed(['jpg', 'png', 'txt'], 'Simple File Types only!!!')
      ]
    )
    model = SelectField(
       u'Select Translation Model', 
       choices=[
         ('ende', 'ende - English to German'), 
         ('kor', 'kor - Korean to English')
       ]
    )
    submit = SubmitField(u'Submit')
