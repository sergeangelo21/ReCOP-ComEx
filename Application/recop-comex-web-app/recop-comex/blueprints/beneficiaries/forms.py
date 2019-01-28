from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField, SubmitField, SelectField, DecimalField, DateField
from wtforms.validators import DataRequired, EqualTo, ValidationError, NumberRange, Email

class ProposalForm(FlaskForm):
	category = SelectField('Category', coerce = int, validators=[DataRequired()])
	title = StringField('Title of the Activity', validators=[DataRequired()])
	description = StringField('Description', validators=[DataRequired()])
	objective = StringField('Objective', validators=[DataRequired()])
	budget = StringField('Proposed Budget', validators=[DataRequired()])
	location = StringField('Venue', validators=[DataRequired()])
	event_date = StringField('Target Date', validators=[DataRequired()])
	submit = SubmitField('Submit')