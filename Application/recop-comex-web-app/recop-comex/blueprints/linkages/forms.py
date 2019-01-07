from flask_wtf import FlaskForm

from wtforms import StringField, TextAreaField, PasswordField, SubmitField, SelectField, DecimalField, DateField
from wtforms.validators import DataRequired, EqualTo, ValidationError, NumberRange, Email

class ProposalForm(FlaskForm):
    title = StringField('Title of the Activity', validators=[DataRequired()])
    date = StringField('Target Date of the Activity', validators=[DataRequired()])
    venue = StringField('Venue', validators=[DataRequired()])
    category = SelectField('Category', choices=[("", "---"),("education","Education"),("environmental","Environmental"),("health","Health"),("livelihood","Livelihood"),("sociopolitical","Sociopolitical"),("spiritual","Spiritual")], validators=[DataRequired()])
    purpose = StringField('Purpose/Objective', validators=[DataRequired()])
    submit = SubmitField('Submit')