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
         ('kor', 'kor - Korean to English'),
         ('enko', 'enko - English to Korean'),
         ('ende', 'ende - English to German') 
       ]
    )
    submit = SubmitField(u'Submit')
