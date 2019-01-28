from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField, SubmitField, SelectField, DecimalField, DateField
from wtforms.validators import DataRequired, EqualTo, ValidationError, NumberRange, Email

class SearchForm(FlaskForm):

	search = StringField("Search", validators=[DataRequired()])
	submit = SubmitField("Search")

