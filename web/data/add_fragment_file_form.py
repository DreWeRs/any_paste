from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired
from wtforms import FileField, SubmitField
from wtforms.fields.simple import StringField
from wtforms.validators import DataRequired


class AddFragmentFileForm(FlaskForm):
    filename = StringField('filename', validators=[DataRequired()])
    file = FileField('file', validators=[FileRequired()])
    submit = SubmitField('Submit')